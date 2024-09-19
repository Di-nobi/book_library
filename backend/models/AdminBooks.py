from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.models import Base
import uuid

class Book(Base):
    __tablename__ = 'books'
    id = Column(String(128), primary_key=True)
    title = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    due_date = Column(String(50), nullable=True)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=True)
    user = relationship('User', back_populates='book')
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.title = kwargs.get('title')
        self.publisher = kwargs.get('publisher')
        self.category = kwargs.get('category')
        self.available = kwargs.get('available')
        self.due_date = kwargs.get('due_date')