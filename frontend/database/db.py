"""Database setup for the library management application"""

from models.books import Book
from models.users import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

class Database:
    def __init__(self):
        self.__engine = create_engine('sqlite:///frontend_library.db')
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
        self.begin_session().add(num)
    

    def save(self):
        self.begin_session().commit()
    

    def add_users(self, **kwargs):
        users = User(**kwargs)
        self.begin_session().add(users)
        self.begin_session().commit()
        return users
    
    def get_publisher(self, publisher):
        return self.begin_session().query(Book).filter(Book.publisher == publisher).first()
    
    def get_category(self, category):
        return self.begin_session().query(Book).filter(Book.category == category).first()

    def add_books(self, **kwargs):
        books = Book(**kwargs)
        self.add(books)
        self.save()
        return books
    
    def delete(self):
        return self.begin_session().delete()

    def get_books(self):
        return self.begin_session().query(Book).all()
    

    def get_book_by_id(self, id):
        return self.begin_session().query(Book).filter(Book.id == id).first()
    
    def get_users_by_id(self, id):
        return self.begin_session().query(User.id == id).first()