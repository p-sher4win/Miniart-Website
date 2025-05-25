from mongoengine import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



# MONGO DB MODELS
# USERS MODEL
class Users(Document, UserMixin):
    meta = {'collection': 'users'}
    name = StringField(required=True, max_length=150)
    username = StringField(required=True, unique=True, max_length=150)
    email = StringField(required=True, unique=True, max_length=150)
    date_added = DateTimeField(default=datetime.utcnow)
    # PASSWORD HASHING
    password_hash = StringField(required=True, max_length=512)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)

    # CREATE A STRING
    def __repr__(self):
        return f"<User {self.username}>"
    

# CATEGORIES MODEL
class Categories(Document):
    meta = {'collection': 'categories'}
    type = StringField(required=True, unique=True, max_length=255)

    # CREATE A STRING
    def __repr__(self):
        return f"<Category {self.type}>"


# PRODUCTS MODEL
class Products(Document):
    meta = {'collection': 'products'}
    title = StringField(required=True, max_length=255)
    price = FloatField(required=True)
    img_urls = ListField(StringField(), required=True, default=[])
    detail = StringField()
    date_added = DateTimeField(default=datetime.utcnow)
    date_updated = DateTimeField(default=datetime.utcnow)
    # RELATIONSHIP WITH CATEGORIES MODEL
    category = ReferenceField(Categories, reverse_delete_rule=NULLIFY)
    # BESTSELLER BOOLEAN
    bestseller = BooleanField(default=False)

    # CREATE A STRING
    def __repr__(self):
        return f"<Product {self.title}>"
    

# FEEDBACK MODEL
class Feedback(Document):
    meta = {'collection': 'feedback'}
    name = StringField(required=True, max_length=150)
    phone_number = StringField(required=True, max_length=150)
    message = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)

    # CREATE A STRING
    def __repr__(self):
        return f"<Feedback {self.name}>"
    

# CUSTOMER REVIEW MODEL
class Review(Document):
    meta = {'collection': 'reviews'}
    name = StringField(require=True)
    title = StringField(required=True)
    review = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    # CREATE A STRING
    def __repr__(self):
        return f"<Review {self.title}>"