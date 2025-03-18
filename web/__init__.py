from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os



# INITIALIZE DB GLOBALLY
db = SQLAlchemy()

# DB_NAME = 'miniart-db.db'
# DB_NAME = 'miniart_db'

# INITIALIZE MIGRATE
migrate = Migrate()

# LOGIN MANAGER CLASS
login_manager = LoginManager()


def create_app():
    # CREATE A FLASK INSTANCE
    app = Flask(__name__)
    app.config.from_object('config.Config')

    print(app.config.get('FLASK_DEBUG'))


    # SECRET KEY
    # app.config['SECRET_KEY'] = os.environ.get()


    # SQLALCHEMY URI CONNECTION
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


    # MYSQL URI CONNECTION
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:2002@localhost/{DB_NAME}'


    # INITIALE DATABASE IN APP
    db.init_app(app)
    # MIGRATE CHANGES TO DB
    migrate.init_app(app, db)

    
    # IMPORT ROUTE BLUEPRINTS
    from .auth import auth
    from .root import root
    from .routes import routes
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(routes, url_prefix='/')


    # CALL CREATE DB FUNCTION
    # FOR SQLITE
    # create_database(app)

    # FOR MYSQL
    create_mysql_db(app)


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
        return Users.query.get(int(user_id))


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



# CREATE SQLITE DB FILE
# def create_database(app):
#     if not path.exists('web/' + DB_NAME):
#         with app.app_context():
#             db.create_all()


# CREATE MYSQL DATABASE
def create_mysql_db(app):
    with app.app_context():
        db.create_all()
        from .models import Users

        # FETCH ID 1 FROM DB
        first_user = Users.query.get(1)

        # IF ID-1 EXISTS
        if first_user:
            
            # IF ID-1.USERNAME NOT admin
            if first_user.username != "admin":

                # DELETE ALL EXISITING USERS IF ANY
                existing_users = Users.query.count()
                if existing_users > 0:
                    db.session.query(Users).delete()
                    db.session.commit()
                    print("✅ Deleted All Existing Users!")

                # INSERT ADMIN VALUES
                admin = Users(name="Admin",
                              username="admin",
                              email="admin@minitart.com",
                              password_hash=generate_password_hash("admin"))
                
                # ADD & COMMIT ADMIN RECORD TO DATABASE
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin User Created!! ID - 1")
            
            # IF ID-1.USERNAME IS admin
            else:
                print("✅ Admin User Already Exists!")

        # IF ID-1 NOT EXISTS
        else:
            existing_users = Users.query.count()
            if existing_users > 0:
                db.session.query(Users).delete()
                db.session.commit()
                print("✅ Deleted All Existing Users!")

            # INSERT ADMIN VALUES
            admin = Users(id=1,
                          name="Admin",
                          username="admin",
                          email="admin@minitart.com",
                          password_hash=generate_password_hash("admin"))
            
            # ADD & COMMIT ADMIN RECORD TO DATABASE
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin User Created!! ID - 1")