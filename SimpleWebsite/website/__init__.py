from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbdjdkj jauhiwje'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #import the blueprints
    from .views import views
    from .auth import auth
       
    #register blueprints
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    print('Attempting to create database...')
    db_path = path.abspath('website/' + DB_NAME)
    print('Database path:', db_path)

    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
        print('Created Database!')
    else:
        print('Database already exists.')
