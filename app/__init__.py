from flask import Flask
from config import Config
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# SQLAlchemy Setup
Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# flask-login
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

