from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import loging_manager, session



from app import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)


class Users(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    password_hash = Column(String(128), nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, last_name={self.last_name!r})"

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


Base.metadata.create_all(bind=engine)


@loging_manager.load_user
def load_user(user_id):
    pass
