from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .webforms import ProductForm, SearchForm, CategoryForm
from .models import Products, Users, Categories
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from bson import ObjectId
from datetime import datetime



root = Blueprint('root', __name__)


# SEARCH ENGINE
@root.route('/search', methods=['POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        search_term = form.search_for.data

        products = Products.objects(title__icontains=search_term).order_by('title')

        return render_template('view/search_products.html',
                               form=form,
                               search_for=search_term,
                               products=products)


# DASHBOARD PAGE
@root.route('/dashboard')
@login_required
def dashboard():
    products_count = Products.objects.count()
    users_count = Users.objects.count()
    category_count = Categories.objects.count()

    return render_template('view/dashboard.html',
                           users_count = users_count,
                           products_count=products_count,
                           category_count=category_count)


# SHOW ALL EXISTING PRODUCTS
@root.route('/inventory')
@login_required
def inventory():

    form = SearchForm()

    # GET ALL EXISTING PRODUCTS FROM DB
    products = Products.objects.order_by('-date_added')

    return render_template('view/inventory.html',
                           products=products,
                           form=form)


# LIST ALL EXISTING CATEGORIES
@root.route('/category/list')
@login_required
def list_categories():

    # GET ALL EXISTING PRODUCTS FROM DB
    categories = Categories.objects.order_by('type')

    return render_template('view/display_categories.html',
                           categories=categories)


# ADD CATEGORY
@root.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        try:
            category = Categories(type=form.type.data)

            # INSERT CATEGORY TO DB
            category.save()
            flash("Category Added!", category='success')
            form.type.data = ''
            return render_template('view/add_category.html',
                            form=form)
        
        except NotUniqueError:
            flash("Category already exists. Please enter a different name.", category='error')

        except ValidationError as ve:
            flash(f"Validation error: {str(ve)}", category='error')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", category='error')

    return render_template('view/add_category.html',
                           form=form)


# EDIT/UPDATE CATEGORY
@root.route('/category/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    form = CategoryForm()

    try:
        category_to_update = Categories.objects.get(id=id)
    except DoesNotExist:
        flash("Category not found!", category='error')
        return redirect(url_for('root.list_categories'))

    if request.method == 'POST':
        category_to_update.type = request.form['type']

        try:
            # UPDATE IN DB
            category_to_update.save()
            
            # RETURN A MESSAGE
            flash("Category Updated!", category='success')
            return redirect(url_for('root.list_categories'))

        except:
            flash("Error Updating! Try again...", category='error')
            return redirect(url_for('root.list_categories'))

    return render_template('view/update_category.html',
                           form=form,
                           category_to_update=category_to_update)


# DELETE CATEGORY
@root.route('/category/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(id):

    try:
        category_to_delete = Categories.objects.get(id=id)
        category_to_delete.delete()

        # RETURN A MESSAGE
        flash("Category Deleted!", category='success')
        return redirect(url_for('root.list_categories'))
    
    except DoesNotExist:
        flash("Category not found!", category='error')
        return redirect(url_for('root.list_categories'))

    except:
        flash("Error Deleting! Try Again...", category='error')
        return redirect(url_for('root.list_categories'))


# ADD PRODUCT
@root.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()

    categories = Categories.objects.all()
    form.category_id.choices = [('', '-- select --')] + [(str(c.id), c.type) for c in categories]

    # VALIDATE FORM
    if form.validate_on_submit():
        
        category = None
        if form.category_id.data:
            try:
                if form.category_id.data:
                    category = Categories.objects.get(id=ObjectId(form.category_id.data))
            except Exception as e:
                flash("Invalid Category Selected!", category='error')
                return render_template('view/add_product.html', form=form)

        img_urls_list = [url.strip() for url in form.img_urls.data.split(',') if url.strip()]

        try:
            product = Products(
                title=form.title.data,
                price=form.price.data,
                img_urls=img_urls_list,
                detail=form.detail.data or "",
                category=category,
                bestseller=form.bestseller.data or False
            )

            # INSERT PRODUCT RECORD TO DB
            product.save()
            flash("Product Added!", category='success')
            return render_template('view/add_product.html',
                           form=form)
        
        except NotUniqueError:
            flash("Product with this title already exists. Please use a different title.", category='error')

        except ValidationError as ve:
            flash(f"Validation Error: {str(ve)}", category='error')

        except Exception as e:
            flash(f"Unexpected error occurred: {str(e)}", category='error')
    
    else:
        if form.errors:
            print(f"\n {form.errors}\n")

    return render_template('view/add_product.html',
                           form=form)


# EDIT/UPDATE PRODUCT
@root.route('/product/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    form = ProductForm()
    
    categories = Categories.objects.all()
    form.category_id.choices = [('', '-- select --')] + [(str(c.id), c.type) for c in categories]

    try:
        product_to_update = Products.objects.get(id=ObjectId(id))
    except DoesNotExist:
        flash("Product not found!", category='error')
        return redirect(url_for('root.inventory'))

    if request.method == 'GET':
        form.title.data = product_to_update.title
        form.price.data = product_to_update.price
        form.img_urls.data = ', '.join(product_to_update.img_urls)
        form.detail.data = product_to_update.detail
        form.category_id.data = str(product_to_update.category.id) if product_to_update.category else ''
        form.bestseller.data = product_to_update.bestseller
    
    if form.validate_on_submit():

        img_urls_list = [url.strip() for url in form.img_urls.data.split(',') if url.strip()]

        product_to_update.title = form.title.data
        product_to_update.price = form.price.data
        product_to_update.img_urls = img_urls_list
        product_to_update.detail = form.detail.data
        product_to_update.bestseller = form.bestseller.data or False
        product_to_update.date_updated = datetime.utcnow()

        if form.category_id.data:
            try:
                selected_category = Categories.objects.get(id=ObjectId(form.category_id.data))
                product_to_update.category = selected_category
            except DoesNotExist:
                flash("Selected category not found!", category='error')
                return redirect(url_for('root.edit_product', id=id))
        else:
            product_to_update.category = None

        try:
            # UPDATE IN DB
            product_to_update.save()

            # RETURN A MESSAGE
            flash("Product Updated!", category='success')
            return redirect(url_for('root.product',
                                id=str(product_to_update.id)))

        except:
            flash("Error Updating! Try again...", category='error')
            return redirect(url_for('root.edit_product',
                                id=str(product_to_update.id)))

    return render_template('view/update_product.html',
                           form=form,
                           product_to_update=product_to_update)


# GET A PRODUCT DETAILS
@root.route('/product/<string:id>')
@login_required
def product(id):

    # GET PRODUCT BY ID
    try:
        product = Products.objects.get(id=id)
    except DoesNotExist:
        flash("Product not found!", category='error')
        return redirect(url_for('root.inventory'))

    return render_template('view/product.html',
                           product=product)


# DELETE PRODUCT
@root.route('/product/<string:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    
    try:
        product_to_delete = Products.objects.get(id=id)
        product_to_delete.delete()

        # RETURN A MESSAGE
        flash("Product Deleted!", category='success')
        return redirect(url_for('root.inventory'))
    
    except DoesNotExist:
        flash("Product not found!", category='error')
        return redirect(url_for('root.inventory'))

    except:
        flash("Error Deleting! Try Again...", category='error')
        return redirect(url_for('root.inventory'))