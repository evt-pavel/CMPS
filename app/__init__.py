from flask import Flask
from config import Config
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from flask_login import LoginManager
from contextlib import contextmanager


# app = Flask(__name__)
# app.config.from_object(Config)

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker()


@contextmanager
def scoped_session():
    session = Session(bind=engine, expire_on_commit=False)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# from app.auth import bp as auth_bp
# app.register_blueprint(auth_bp, url_prefix='/auth')
#
# from app.main import bp as main_bp
# app.register_blueprint(main_bp)

# flask-login
# login = LoginManager(app)
# login.login_view = 'auth.login'

#
# from app import models


##############################################

login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from app import models






