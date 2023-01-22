from flask import Flask
from config import Config
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from flask_login import LoginManager
from flask_admin import Admin
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session


app = Flask(__name__)
app.config.from_object(Config)

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)
#Session = sessionmaker()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# @contextmanager
# def session_scope():
#     session = Session(bind=engine,  expire_on_commit=False)
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()


# flask-login
login = LoginManager(app)
login.login_view = 'login'

# flask-admin
admin = Admin(app, name='CMP_SHOP', template_mode='bootstrap3')


from app import routes, models




