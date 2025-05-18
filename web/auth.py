from flask import Blueprint, render_template, flash, request, redirect, url_for
from .webforms import UserForm, LoginForm, PasswordForm
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from mongoengine.errors import DoesNotExist
from bson import ObjectId



auth = Blueprint('auth', __name__)


# LOGIN USER
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # VALIDATE FORM FOR LOGIN
    if form.validate_on_submit():
        user = Users.objects(username=form.username.data).first()

        if user:
            # CHECK PASSWORD HASH
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                if user.username == "admin":
                    flash("Welcome Admin!", category='success')
                else:
                    flash(f"Welcome {user.username} - Logged In!", category='success')
                return redirect(url_for('root.dashboard'))
            else:
                flash("Wrong Password! - Try Again", category='error')
        else:
            flash("Invalid Username!", category='error')

        # CLEAR FORM
        form.username.data = ''

    return render_template('view/login.html',
                           form=form)


# LOGOUT USER
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged Out!", category='success')
    return redirect(url_for('routes.home'))


# REGISTER USER
@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    name = None
    form = UserForm()

    # CHECK IF ADMIN
    if current_user.username == "admin": 
    # VALIDATE FORM DATA
        if form.validate_on_submit():
            # QUERY DB FOR CHECKING IF USER ALREADY EXISTS
            user = Users.objects(username=form.username.data).first()
            
            if user is None:
                # HASH PASSWORD
                hashed_pw = generate_password_hash(form.password_hash.data)

                # USER DATA TO INSERT INTO DB
                user = Users(name=form.name.data,
                            username=form.username.data,
                            email=form.email.data,
                            password_hash=hashed_pw)
                
                # INSERT RECORD INTO DB
                user.save()

            # ASSIGN NAME VALUE
            name = form.name.data

            # CLEAR FORM
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''

            # RETURN A MESSAGE
            flash("User Registered!", category='success')
            return redirect(url_for('auth.users'))

        our_users = Users.objects.order_by('-date_added')

        return render_template('view/register.html',
                            form=form,
                            name=name,
                            our_users=our_users)
    
    else:
        flash("Sorry! You Are Not Authorized For This Action...", category='error')
        return redirect(url_for('root.dashboard'))


# EDIT/UPDATE USER
@auth.route('/user/<string:id>/update', methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = UserForm()

    try:
        name_to_update = Users.objects.get(id=ObjectId(id))
    except DoesNotExist:
        flash("User not found", category='error')
        return redirect(url_for('root.dashboard'))

    if request.method == 'POST':

        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']

        try:
            name_to_update.save()
            flash("User Updated!", category='success')
            return redirect(url_for('root.dashboard'))

        except:
            flash("Error Updating User!", category='error')
            return render_template('view/update_user.html',
                                form=form,
                                name_to_update=name_to_update)
    else:
        return render_template('view/update_user.html',
                            form=form,
                            name_to_update=name_to_update,
                            id=id)
    

# DELETE USER
@auth.route('/user/<string:id>/delete')
@login_required
def delete_user(id):

    # ONLY ADMIN AND THE SPECIFIC ID USER CAN DELETE THEIR PROFILE
    if str(current_user.id) == id or current_user.username == 'admin':
        try:
            user_to_delete = Users.objects.get(id=ObjectId(id))
            user_to_delete.delete()

            if current_user.username == 'admin':
                flash("User Deleted!", category='success')
                return redirect(url_for('auth.users'))
            else:
                logout_user()
                flash("Account Deleted! Logged Out!", category='success')
                return redirect(url_for('routes.home'))

        except DoesNotExist:
            flash("User Not Found!", category='error')
            return redirect(url_for('auth.users'))
        
    else:
        flash("You Don't Have Access To This User", category='error')
        return redirect(url_for('root.dashboard'))


# RESET USER PASSWORD
@auth.route('/user/<string:id>/password-reset', methods=['GET', 'POST'])
@login_required
def reset_password(id):
    form = PasswordForm()

    try:
        user_password_reset = Users.objects.get(id=ObjectId(id))
    except DoesNotExist:
        flash("User Not Found", category='error')
        return redirect(url_for('auth.users'))

    if form.validate_on_submit():
        reset_hashed_pw = generate_password_hash(form.reset_password_hash.data)

        user_password_reset.password_hash = reset_hashed_pw

        try:
            user_password_reset.save()
            flash("Password Changed!", category='success')
            return redirect(url_for('root.dashboard'))
        
        except:
            flash("Error Changing Password!", category='error')
            return render_template('view/change_user_password.html',
                                   form=form)

    else:
        return render_template('view/change_user_password.html',
                           form=form,
                           id=id,
                           user_password_reset=user_password_reset)
    

# DISPLAY ALL USERS
@auth.route('/users')
@login_required
def users():

    # GET ALL EXISTING USERS FROM DB
    users = Users.objects.order_by('-date_added')

    return render_template('view/display_users.html',
                           users=users)