from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Products, Feedback, Categories
from .webforms import FeedbackForm
from mongoengine.errors import DoesNotExist
from bson import ObjectId



routes = Blueprint('routes', __name__)


# HOME PAGE
@routes.route('/')
def home():

    bestsellers = Products.objects.order_by('title')

    return render_template('view/home.html',
                           bestsellers=bestsellers)


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

    category = Categories.objects()

    return render_template('view/store.html',
                           category=category)


# PRODUCT UNDER A CATEGORY
@routes.route('/category/<string:id>')
def category(id):
    try:
        category = Categories.objects.get(id=ObjectId(id))
        products = Products.objects(category=category)

    except Categories.DoesNotExist:
        flash("Category Not Found!", category='error')
        return redirect(url_for('routes.store'))

    return render_template('view/category_product.html',
                           category=category,
                           products=products)