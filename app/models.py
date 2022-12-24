from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship

from app import Config

Base = declarative_base()
engine = create_engine(Config.DATABASE_URI)


# class Users(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(30))
#     last_name = Column(String(30))
#     email = Column(String(50))
#     password_hash = Column(String(128))
#
#     def __repr__(self):
#         return f"User(id={self.id!r}, name={self.name!r}, last_name={self.last_name!r})"


Base.metadata.create_all(bind=engine)
