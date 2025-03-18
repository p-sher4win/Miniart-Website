from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Products, Feedback
from .webforms import FeedbackForm
from . import db

routes = Blueprint('routes', __name__)


# HOME PAGE
@routes.route('/')
def home():

    bestsellers = Products.query.order_by(Products.title.asc())

    return render_template('home.html',
                           bestsellers=bestsellers)


# STORE PAGE
@routes.route('/store')
def store():
    return render_template('store.html')


# DIGITAL & STATIONERY PAGE
@routes.route('/digital-stationery')
def digital_stationery():
    return render_template('digital_stationery.html')


# FASHION & ACCESSORIES PAGE
@routes.route('/fashion-accessories')
def fashion_accessories():
    return render_template('fashion_accessories.html')


# GIFTS & KEEPSAKES PAGE
@routes.route('/gifts-keepsakes')
def gifts_keepsakes():
    return render_template('gifts_keepsakes.html')


# HANDMADE CANDLES PAGE
@routes.route('/handmade-candles')
def handmade_candles():
    return render_template('handmade_candles.html')


# CRAFTS & FLORAL ART PAGE
@routes.route('/crafts-flora-art')
def crafts_flora_art():

    products = Products.query.order_by(Products.title.asc())
    
    return render_template('crafts_flora_art.html',
                           products=products)


# HOME & WALL DECO PAGE
@routes.route('/home-wall-deco')
def home_wall_deco():
    return render_template('home_wall_deco.html')


# INDIVIDUAL PRODUCT
@routes.route('/item/<int:id>')
def item(id):
    # GET PRODUCT BY ID
    item = Products.query.get_or_404(id)

    return render_template('item.html',
                           item=item)


# ABOUT US PAGE
@routes.route('/about')
def about():
    return render_template('about.html')


# CONTACT US PAGE
@routes.route('/contact', methods=['GET', 'POST'])
def contact():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data,
                            phone_number=form.phone_number.data,
                            message=form.message.data)
        
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback Submitted!", category='success')
        return redirect(url_for('routes.contact'))


    return render_template('contact.html',
                           form=form)