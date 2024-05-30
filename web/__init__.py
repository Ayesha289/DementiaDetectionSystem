from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
DB_NAME = 'data.db'

mail = Mail()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(basedir, 'instance', 'data.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    db.init_app(app)

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'dementiadetectionsystem@gmail.com'
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSCODE')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    
    mail.init_app(app)
    jwt.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, MedHistory
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app