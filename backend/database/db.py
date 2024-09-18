"""Database setup for the library management application"""

from models.AdminBooks import Book
from models.AdminUser import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

class Database:
    def __init__(self):
        self.__engine = create_engine('sqlite:///library.db')
        Base.metadata.create_all(self.__engine)
        self._session = None

    def begin_session(self):
        if self._session is None:
            self._session = scoped_session(sessionmaker(bind=self.__engine))
        return self._session
    
    def close_session(self):
        if self._session is not None:
            self._session.remove()
            self._session = None
        
   
    def add(self, num):
        return self.begin_session().add(num)
    

    def save(self):
        return self.begin_session().commit
    

    def delete(self):
        return self.begin_session().delete
    

    def add_books(self, **kwargs):
        books = Book(**kwargs)
        books.available = True
        self.add(books)
        self.save()
        return books
    
    def get_books(self):
        return self._session.query(Book).all()
    
    def get_book_by_id(self, id):
        return self._session.query(Book).filter(Book.id == id).first()
    
    def get_users_with_books(self):
        """Return all users with books checked out"""
        return self._session.query(User).join(Book).all()
    
    def get_users(self):
        """Returns all users"""
        return self._session.query(User).all()