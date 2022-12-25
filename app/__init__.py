from flask import Flask
from config import Config
from sqlalchemy.orm import sessionmaker
from app.models import Base, Users
from sqlalchemy import create_engine
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

#  SQLAlchemy connect DB and create session
engine = create_engine(Config.DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = DBSession()

#  flask-login
loging_manager = LoginManager()
loging_manager.init_app(app)


from app import routes, models
