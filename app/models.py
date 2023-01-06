from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, DECIMAL
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


class Part(Base):
    #запчасть
    __tablename__ = 'part'

    id = Column(Integer, primary_key=True)
    part_number = Column(String)
    description = Column(String)  # полное название детали
    price = Column(Integer)
    amount = Column(Integer)
    brand = relationship('Brand')
    type = relationship('Type')
    model = relationship('Model')
    element = relationship('Element')


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(30))
    part_id = Column(Integer, ForeignKey('part.id'))
    parent = relationship('Part', back_populates='brand')


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    type_name = Column(String)
    part_id = Column(Integer, ForeignKey('part.id'))
    parent = relationship('Part', back_populates='type')


class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    part_id = Column(Integer, ForeignKey('part.id'))
    parent = relationship('Part', back_populates='model')


class Element(Base):
    # technical drawings
    __tablename__ = 'element'

    id = Column(Integer, primary_key=True)
    element_name = Column(String)
    part_id = Column(Integer, ForeignKey('part.id'))
    parent = relationship('Part', back_populates='element')


@login.user_loader
def load_user(id):
    return session.query(User).get(int(id))