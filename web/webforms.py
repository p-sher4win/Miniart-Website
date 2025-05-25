from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FloatField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea



# WEB FORMS
# CREATE LOGIN FORM
class LoginForm(FlaskForm):
    username = StringField("Userame", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("LOGIN")


# CREATE USER FORM
class UserForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired()])
    username = StringField("Userame", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message="Password Doesn't Match!")])
    password_hash2 = PasswordField("Password (Confirm)", validators=[DataRequired()])
    add = SubmitField("REGISTER")
    update = SubmitField("UPDATE")


# CREATE PRODUCT CATEGORY FORM
class CategoryForm(FlaskForm):
    type = StringField("Input Category Type", validators=[DataRequired()])
    create = SubmitField("CREATE CATEGORY")
    update = SubmitField("UPDATE CATEGORY")



# CREATE PRODUCT FORM
class ProductForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    price = FloatField("Price (₹)", validators=[DataRequired()])
    img_urls = TextAreaField("Image URLs (comma-separated)", widget=TextArea(), validators=[DataRequired()])
    detail = TextAreaField("Description", widget=TextArea())
    bestseller = BooleanField("Best Seller", default=False)
    # DORPDOWN FOR SELECTING CATEGORY
    category_id = SelectField("Category", choices=[], coerce=str, validate_choice=False)
    add = SubmitField("ADD")
    update = SubmitField("UPDATE")


# CREATE PASSWORD RESET FORM
class PasswordForm(FlaskForm):
    reset_password_hash = PasswordField("Password (Change)", validators=[DataRequired(), EqualTo('reset_password_hash2', message="Password Doesn't Match!")])
    reset_password_hash2 = PasswordField("Password (Confirm Change)", validators=[DataRequired()])
    reset = SubmitField("RESET")


# SEARCH FORM
class SearchForm(FlaskForm):
    search_for = StringField("Searched", validators=[DataRequired()])
    search = SubmitField("Go")


# FEEDBACK FORM
class FeedbackForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    phone_number = StringField("Phone No", validators=[DataRequired()])
    message = TextAreaField("Feedback", widget=TextArea())
    submit = SubmitField("SUBMIT")


# CUSTOMER REVIEW FORM
class ReviewForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    message = TextAreaField("Write a review", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("SUBMIT")
    