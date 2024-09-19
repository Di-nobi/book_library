from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from frontend.models import Base
import uuid

class Book(Base):
    __tablename__ = 'books'
    id = Column(String(128), primary_key=True)
    title = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    due_date = Column(String(50))
    user_id = Column(String(128), ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='book')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.publisher = kwargs.get('publisher')
        self.category = kwargs.get('category')
        self.available = kwargs.get('available')
        self.user_id = kwargs.get('user_id')