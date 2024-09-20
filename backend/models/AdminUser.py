from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models import Base
import uuid

class User(Base):
    __tablename__ = 'users'
    id = Column(String(128), primary_key=True)
    email = Column(String(255), nullable=False)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    books = relationship('Book', back_populates='user')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        self.firstName = kwargs.get('firstName')
        self.lastName = kwargs.get('lastName')