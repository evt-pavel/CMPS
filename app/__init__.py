from flask import Flask
from config import Config
from sqlalchemy.orm import sessionmaker
from app.models import Base, Users
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object(Config)
engine = create_engine(Config.DATABASE_URI)
DBSession = sessionmaker(bind=engine)
session = DBSession()


from app import routes, models
