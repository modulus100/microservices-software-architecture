from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random
import string

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase +
                                   string.digits) for x in xrange(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))
    email = Column(String(254))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(String)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
        'name' : self.name,
        'category' : self.category,
        'price' : self.price
            }

engine = create_engine('sqlite:///catalogApp.db')
 

Base.metadata.create_all(engine)