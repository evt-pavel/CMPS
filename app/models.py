from sqlalchemy import Column, ForeignKey, Integer, String, DATE
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import Base, session, login, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView



class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(50), nullable=False)
    password_hash = Column(String(128), nullable=False)
    parent = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, last_name={self.last_name!r})"

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Part(Base):
    __tablename__ = 'part'

    id = Column(Integer, primary_key=True)
    part_number = Column(String)
    description = Column(String)  # полное название детали
    price = Column(Integer)
    amount = Column(Integer)

    model_id = Column(Integer, ForeignKey('model.id'),  nullable=False)
    model = relationship('Model', back_populates="parent")

    element_id = Column(Integer, ForeignKey('element.id'), nullable=False)
    element = relationship('Element', back_populates="parent")

    parent = relationship('Basket', back_populates='part')   # переделать

    def __repr__(self):
        return (self.description)



class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(30))
    parent = relationship('Model', back_populates='brand')

    def __repr__(self):
        return (self.brand_name)



class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    type_name = Column(String)
    parent = relationship('Model', back_populates='type')

    def __repr__(self):
        return (self.type_name)


class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    model_name = Column(String)

    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    brand = relationship('Brand', back_populates="parent")

    type_id = Column(Integer, ForeignKey('type.id'), nullable=False)
    type = relationship('Type', back_populates="parent")

    parent = relationship('Part', back_populates='model')
    
    image_id = Column(Integer, ForeignKey('element_image.id'))
 

    def __repr__(self):
        return (self.model_name)


class Element(Base):
    # technical drawings
    __tablename__ = 'element'

    id = Column(Integer, primary_key=True)
    element_name = Column(String)
    parent = relationship('Part', back_populates='element')
    # image = relationship('ElementImage', back_populates='element')
    image_id = Column(Integer, ForeignKey('element_image.id'))

    def __repr__(self):
        return (self.element_name)


class ElementImage(Base):
    __tablename__ = 'element_image'

    id = Column(Integer, primary_key=True)
    url = Column(String)

    model = relationship('Model')
    element = relationship('Element')


class Order(Base):
    __tablename__ = 'order'

    id = Column (Integer, primary_key=True)
    address = Column(String)
    status = Column(Integer)
    date_order = Column(DATE)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='parent')

    parent = relationship('Basket', back_populates='order')


class Basket(Base):
    __tablename__ = 'basket'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)

    part_id = Column(Integer, ForeignKey('part.id'))
    part = relationship('Part', back_populates='parent')

    order_id = Column(Integer, ForeignKey('order.id'))
    order = relationship('Order', back_populates='parent')


@login.user_loader
def load_user(id):
    user = session.query(User).get(int(id))
    return user




admin.add_view(ModelView(User, session, name='Пользователи'))
admin.add_view(ModelView(Brand, session, name='Бренды'))
admin.add_view(ModelView(Type, session, name='Тип ТС'))
admin.add_view(ModelView(Model, session, name='Модели'))
admin.add_view(ModelView(Element, session, name='Схемы'))
admin.add_view(ModelView(Part, session, name='Запчасти'))
admin.add_view(ModelView(ElementImage, session, name='Картинка Схемы'))






