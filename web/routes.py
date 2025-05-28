from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Products, Feedback, Categories, Review
from .webforms import FeedbackForm, ReviewForm
from mongoengine.errors import DoesNotExist
from bson import ObjectId
import random
from datetime import datetime



routes = Blueprint('routes', __name__)


# HOME PAGE
@routes.route('/')
def home():

    bestsellers = Products.objects.order_by('title')
    reviews = Review.objects()[:2]

    return render_template('view/home.html',
                           bestsellers=bestsellers,
                           reviews=reviews)


# INDIVIDUAL PRODUCT
@routes.route('/item/<string:id>')
def item(id):

    # GET PRODUCT BY ID
    try:
        item = Products.objects.get(id=ObjectId(id))
    except DoesNotExist:
        flash("Product not found!", category='error')
        return redirect(url_for('routes.home'))

    return render_template('view/item.html',
                           item=item)


# ABOUT US PAGE
@routes.route('/about')
def about():
    return render_template('view/about.html')


# CONTACT US PAGE
@routes.route('/contact', methods=['GET', 'POST'])
def contact():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data,
                            phone_number=form.phone_number.data,
                            message=form.message.data)
        
        feedback.save()
        flash("Feedback Submitted!", category='success')
        return redirect(url_for('routes.contact'))

    return render_template('view/contact.html',
                           form=form)


# STORE PAGE
@routes.route('/store')
def store():

    categories = list(Categories.objects())

    first_category = None
    other_categories = []

    for category in categories:
        if category.type.lower() == "quick customization":
            first_category = category
        else:
            other_categories.append(category)

    if first_category:
        ordered_categories = [first_category] + other_categories
    else:
        ordered_categories = other_categories

    return render_template('view/store.html',
                           category=ordered_categories)


# PRODUCT UNDER A CATEGORY
@routes.route('/category/<string:id>')
def category(id):
    try:
        category = Categories.objects.get(id=ObjectId(id))

        if category.type.lower() == "quick customization":
            return render_template('view/quick_custom.html',
                                   category=category)

        products = list(Products.objects(category=category))
        random.shuffle(products)

    except Categories.DoesNotExist:
        flash("Category Not Found!", category='error')
        return redirect(url_for('routes.store'))

    return render_template('view/category_product.html',
                           category=category,
                           products=products)


# CUSTOMER REVIEW
@routes.route('/write_review', methods=['GET', 'POST'])
def review_form():
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            name=form.name.data,
            title=form.title.data,
            review=form.message.data
        )

        review.save()
        flash("Review Added!", category='success')
        return redirect(url_for('routes.get_reviews'))

    return render_template('view/review_form.html',
                           form=form)


# DISPLAY CUSTOMER REVIEWS
@routes.route('/reviews')
def get_reviews():

    reviews = Review.objects.order_by('-timestamp')
    reviews_count = Review.objects.count()

    for review in reviews:
        review.formatted_date = review.timestamp.strftime("%d %B %Y")

    return render_template('view/reviews.html',
                           reviews=reviews,
                           reviews_count=reviews_count)