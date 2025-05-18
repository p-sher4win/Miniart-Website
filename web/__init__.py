from flask import Flask, render_template
import mongoengine
from bson.objectid import ObjectId
from flask_login import LoginManager
from werkzeug.security import generate_password_hash



# LOGIN MANAGER CLASS
login_manager = LoginManager()


def create_app():
    # CREATE A FLASK INSTANCE
    app = Flask(__name__)
    app.config.from_object('config.Config')


    # INITIALE DATABASE IN APP
    mongoengine.connect(
        db='miniart_db',
        host=app.config['MONGO_URI']
    )

    
    # IMPORT ROUTE BLUEPRINTS
    from .auth import auth
    from .root import root
    from .routes import routes
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')


    # CALL CREATE DB FUNCTION
    # FOR MONGODB
    create_mongo_db(app)


    # LOGIN MANAGER CONFIG
    # INITIALIZE LM
    login_manager.init_app(app)
    
    # CUSTOMIZE LM
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page!"
    login_manager.login_message_category = 'warning'

    # IMPORT USERS MODEL
    from .models import Users

    # LOAD USERS
    @login_manager.user_loader
    def load_user(user_id):
        return Users.objects.get(id=ObjectId(user_id))


    # CREATE CUSTOM ERROR PAGES
    # NOT FOUND ERROR
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template ('404.html'), 404

    # INTERNAL SERVER ERROR
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template ('500.html'), 500


    return app



# CREATE MONGO DB
def create_mongo_db(app):
    with app.app_context():
        from .models import Users

        # FETCH FIRST USER FROM DB
        first_user = Users.objects.first()

        if first_user:
            # CHECK IF USER IS ADMIN
            if first_user.username != "admin":
                Users.objects.delete() # DELETES ALL EXISTING USERS
                print("\n✅ Deleted All Existing Users!\n")
                
                # CREATE ADMIN USER
                admin = Users(name="Admin",
                              username="admin",
                              email="admin@miniart.com",
                              password_hash=generate_password_hash("admin"))
                admin.save()
                print("\n✅ Admin User Created!\n")

            else:
                print("\n✅ Admin User Already Exists!\n")

        else:
            # INSERT VALUES TO CREATE ADMIN USER
            admin = Users(name="Admin",
                              username="admin",
                              email="admin@miniart.com",
                              password_hash=generate_password_hash("admin"))
            admin.save()
            print("\n✅ Admin User Created!\n")