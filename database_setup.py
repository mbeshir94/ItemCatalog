import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


# store user data
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    image = Column(String(150))
    provider = Column(String(20))

# Categories Database
class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name
        }

# Books Database
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    bookName = Column(String(150), nullable=False)
    authorName = Column(String(150), nullable=False)
    coverUrl = Column(String(500), nullable=False)
    description = Column(String(), nullable=False)
    category = Column(String(150), ForeignKey('categories.name'))
    category_rel =  relationship(CategoryDB)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.bookName,
            'author': self.authorName,
            'genre': self.category,
            'coverUrl': self.coverUrl,
            'description': self.description
        }

engine = create_engine('sqlite:///BookCatalog.db')
Base.metadata.create_all(engine)
