from flask import Flask
from config import Config
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy import create_engine
from flask_login import LoginManager
from flask_admin import Admin



# sqlalchemy setup
Base = declarative_base()
engine = create_engine(Config.DATABASE_URI, echo=False)
session_factory = sessionmaker(engine, expire_on_commit=False)
session = scoped_session(session_factory)


# flask-login
login = LoginManager()
login.login_view = 'auth.login'
admin = Admin(name='CMP SHOP', template_mode='bootstrap3')




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    admin.init_app(app)


    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models









