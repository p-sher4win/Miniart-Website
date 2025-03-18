from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# DATABASE MODELS
# CREATE USERS MODEL
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # PASSWORD HASHING
    password_hash = db.Column(db.String(512), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # CREATE A STRING
    def __repr__(self):
        return f"<User {self.username}>"
    

# CREATE PRODUCT CATEGORIES MODEL
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=False, unique=True)

    # FORIEGN KEY RELATION WITH PRODUCT MODEL
    products = db.relationship('Products', backref='category')

    def __repr__(self):
        return f"<Category {self.type}>"


# CREATE PRODUCTS MODEL
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # FORIEGN KEY TO LINK CATEGORY MODEL
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # BESTSELLER BOOLEAN
    bestseller = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Product {self.title}>"
    

# CREATE FEEDBACK MODEL
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Feedback {self.name}>"