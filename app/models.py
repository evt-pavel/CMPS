from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import Base, login, session
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'user'

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


@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))