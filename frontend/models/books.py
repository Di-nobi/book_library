from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='book')

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.publisher = kwargs.get('author')
        self.category = kwargs.get('category')
        # self.user_id = kwargs.get('user_id')