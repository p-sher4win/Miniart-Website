from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .webforms import ProductForm, SearchForm, CategoryForm
from .models import Products, Users, Categories
from . import db


root = Blueprint('root', __name__)


# SEARCH ENGINE
@root.route('/search', methods=['POST'])
def search():
    form = SearchForm()

    products = Products.query

    if form.validate_on_submit():
        product.search_for = form.search_for.data

        products = products.filter(Products.title.like('%' + product.search_for + '%'))

        products = products.order_by(Products.title).all()

        return render_template('search_products.html',
                               form=form,
                               search_for=product.search_for,
                               products=products)   


# DASHBOARD PAGE
@root.route('/dashboard')
@login_required
def dashboard():

    products_count = Products.query.count()
    users_count = Users.query.count()
    category_count = Categories.query.count()

    return render_template('dashboard.html',
                           users_count = users_count,
                           products_count=products_count,
                           category_count=category_count)


# SHOW ALL EXISTING PRODUCTS
@root.route('/inventory')
@login_required
def inventory():

    form = SearchForm()

    # GET ALL EXISTING PRODUCTS FROM DB
    products = Products.query.order_by(Products.date_added.desc())

    return render_template('inventory.html',
                           products=products,
                           form=form)


# LIST ALL EXISTING CATEGORIES
@root.route('/category/list')
@login_required
def list_categories():

    # GET ALL EXISTING PRODUCTS FROM DB
    categories = Categories.query.order_by(Categories.type.asc())

    return render_template('display_categories.html',
                           categories=categories)


# ADD CATEGORY
@root.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Categories(type=form.type.data)

        # COMMIT CATEGORY TO DB
        db.session.add(category)
        db.session.commit()
        flash("Category Added!", category='success')
        form.type.data = ''
        return render_template('add_category.html',
                           form=form)


    return render_template('add_category.html',
                           form=form)


# EDIT/UPDATE CATEGORY
@root.route('/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    form = CategoryForm()

    category_to_update = Categories.query.get_or_404(id)

    if request.method == 'POST':
        category_to_update.type = request.form['type']

        try:
            # UPDATE IN DB
            db.session.commit()
            
            # RETURN A MESSAGE
            flash("Category Updated!", category='success')
            return redirect(url_for('root.list_categories',
                                id=category_to_update.id))

        except:
            flash("Error Updating! Try again...", category='error')
            return redirect(url_for('root.list_categories',
                                id=category_to_update.id))

    return render_template('update_category.html',
                           form=form,
                           category_to_update=category_to_update)


# DELETE CATEGORY
@root.route('/category/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    form = CategoryForm()

    category_to_delete = Categories.query.get_or_404(id)

    try:
        db.session.delete(category_to_delete)
        db.session.commit()

        # RETURN A MESSAGE
        flash("Category Deleted!", category='success')
        return redirect(url_for('root.list_categories'))
    
    except:
        flash("Error Deleting! Try Again...", category='error')
        return redirect(url_for('root.list_categories'))


# ADD PRODUCT
@root.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()

    categories = Categories.query.all()
    form.category_id.choices = [(c.id, c.type) for c in categories]

    # VALIDATE FORM
    if form.validate_on_submit():
        category_id = int(form.category_id.data)

        if form.bestseller.data == None:
            form.bestseller.data = False

        product = Products(title=form.title.data,
                            price=form.price.data,
                            img_url=form.img_url.data,
                            detail=form.detail.data,
                            category_id=category_id,
                            bestseller=form.bestseller.data)
        
        # COMMIT PRODUCT RECORD TO DB
        db.session.add(product)
        db.session.commit()
        flash("Product Added!", category='success')
        return redirect(url_for('root.inventory'))

    return render_template('add_product.html',
                           form=form)


# EDIT/UPDATE PRODUCT
@root.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    form = ProductForm()

    categories = Categories.query.all()
    form.category_id.choices = [(c.id, c.type) for c in categories]

    product_to_update = Products.query.get_or_404(id)

    if request.method == 'POST':
        product_to_update.title = request.form['title']
        product_to_update.price = request.form['price']
        product_to_update.img_url = request.form['img_url']
        product_to_update.detail = request.form['detail']
        product_to_update.category_id = int(form.category_id.data)
        product_to_update.bestseller = 'bestseller' in request.form

        try:
            # UPDATE IN DB
            db.session.commit()
            
            # RETURN A MESSAGE
            flash("Product Updated!", category='success')
            return redirect(url_for('root.product',
                                id=product_to_update.id))

        except:
            flash("Error Updating! Try again...", category='error')
            return redirect(url_for('root.product',
                                id=product_to_update.id))

    return render_template('update_product.html',
                           form=form,
                           product_to_update=product_to_update)


# GET A PRODUCT DETAILS
@root.route('/product/<int:id>')
@login_required
def product(id):

    # GET PRODUCT BY ID
    product = Products.query.get_or_404(id)

    return render_template('product.html',
                           product=product)


# DELETE PRODUCT
@root.route('/product/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    form = ProductForm()

    product_to_delete = Products.query.get_or_404(id)

    try:
        db.session.delete(product_to_delete)
        db.session.commit()

        # RETURN A MESSAGE
        flash("Product Deleted!", category='success')
        return redirect(url_for('root.inventory'))

    except:
        flash("Error Deleting! Try Again...", category='error')
        return redirect(url_for('root.inventory'))