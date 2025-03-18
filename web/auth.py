from flask import Blueprint, render_template, flash, request, redirect, url_for
from .webforms import UserForm, LoginForm, PasswordForm
from .models import Users
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


# LOGIN USER
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # VALIDATE FORM FOR LOGIN
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user:
            
            # CHECK PASSWORD HASH
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                if user.username == "admin":
                    flash("Welcome Admin!", category='success')
                else:
                    flash("Welcome User - Logged In!", category='success')
                return redirect(url_for('root.dashboard'))
            else:
                flash("Wrong Password! - Try Again", category='error')
        else:
            flash("Invalid Username!", category='error')

        # CLEAR FORM
        form.username.data = ''

    return render_template('login.html',
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
    if current_user.id == 1: 
    # VALIDATE FORM DATA
        if form.validate_on_submit():

            # QUERY DB FOR CHECKING IF USER ALREADY EXISTS
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:

                # HASH PASSWORD
                hashed_pw = generate_password_hash(form.password_hash.data)

                # USER DATA TO INSERT INTO DB
                user = Users(name=form.name.data,
                            username=form.username.data,
                            email=form.email.data,
                            password_hash=hashed_pw)
                
                # INSERT RECORD INTO DB
                db.session.add(user)
                db.session.commit()

            # ASSIGN NAME VALUE
            name = form.name.data

            # CLEAR FORM
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''

            # RETURN A MESSAGE
            flash("User Registered!", category='success')
            return redirect(url_for('auth.users'))

        our_users = Users.query.order_by(Users.date_added)

        return render_template('register.html',
                            form=form,
                            name=name,
                            our_users=our_users)
    
    else:
        flash("Sorry! You Are Not Authorized For This Action...", category='error')
        return redirect(url_for('root.dashboard'))


# EDIT/UPDATE USER
@auth.route('/user/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = UserForm()

    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':

        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']

        try:
            db.session.commit()
            flash("User Updated!", category='success')
            # return render_template('update_user.html',
            #                     form=form,
            #                     name_to_update=name_to_update)
            return redirect(url_for('root.dashboard'))

        except:
            flash("Error Updating User!", category='error')
            return render_template('update_user.html',
                                form=form,
                                name_to_update=name_to_update)
    else:
        return render_template('update_user.html',
                            form=form,
                            name_to_update=name_to_update,
                            id=id)
    

# DELETE USER
@auth.route('/user/<int:id>/delete')
@login_required
def delete_user(id):

    # ONLY ADMIN AND THE SPECIFIC ID USER CAN DELETE THEIR PROFILE
    if id == current_user.id or id == 1 or current_user.id == 1:
        name = None
        form = UserForm()
        user_to_delete = Users.query.get_or_404(id)

        try:
            db.session.delete(user_to_delete)
            db.session.commit()

            if current_user.id == 1:
                flash("User Deleted!", category='success')
                return redirect(url_for('auth.users'))
            else:
                flash("Account Deleted! Logged Out!", category='success')
                return redirect(url_for('routes.home'))

        except:
            flash("Error Deleting User!", category='error')
            return redirect(url_for('auth.users'))
        
    else:
        flash("You Don't Have Access To This User", category='error')
        return redirect(url_for('root.dashboard'))


# RESET USER PASSWORD
@auth.route('/user/<int:id>/password-reset', methods=['GET', 'POST'])
@login_required
def reset_password(id):
    form = PasswordForm()

    user_password_reset = Users.query.get_or_404(id)

    if request.method == 'POST':
        reset_hashed_pw = generate_password_hash(request.form['reset_password_hash'])

        user_password_reset.password_hash = reset_hashed_pw

        try:
            db.session.commit()
            flash("Password Changed!", category='success')
            return redirect(url_for('root.dashboard'))
        
        except:
            flash("Error Changing Password!", category='error')
            return render_template('change_user_password.html',
                                   form=form)

    else:
        return render_template('change_user_password.html',
                           form=form,
                           id=id,
                           user_password_reset=user_password_reset)
    

# DISPLAY ALL USERS
@auth.route('/users')
@login_required
def users():

    # GET ALL EXISTING USERS FROM DB
    users = Users.query.order_by(Users.date_added.desc())

    return render_template('display_users.html',
                           users=users)

