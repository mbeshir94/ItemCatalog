from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BookDB, User, CategoryDB
from sqlalchemy.pool import SingletonThreadPool
import os

engine = create_engine('postgresql://postgres:postgres@localhost/BookCatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(id="1", name="admin", email="mahmoud.beshir94@gmail.com")
session.add(User1)
session.commit()

# Create categories

category1 = CategoryDB(id=1, name="Fantasy")

session.add(category1)
session.commit()

category2 = CategoryDB(id=2, name="Romance")

session.add(category2)
session.commit()

category3 = CategoryDB(id=3, name="Mystery")

session.add(category3)
session.commit()

category4 = CategoryDB(id=4, name="Fiction")

session.add(category4)
session.commit()

category5 = CategoryDB(id=5, name="Horror")

session.add(category5)
session.commit()

category6 = CategoryDB(id=6, name="Other")

session.add(category6)
session.commit()


# Create dummy books data
book1 = BookDB(id="1", bookName="Hello!",
               authorName="Janine Amos",
               coverUrl="bla bla",
               description="...", category="Other", user_id=1)

session.add(book1)
session.commit()

book2 = BookDB(id="2", bookName="Romantic Poetry, Volume 7",
               authorName="Angela Esterhammer",
               coverUrl="bla bla",
               description="...", category="Romance", user_id=1)

session.add(book2)
session.commit()

book3 = BookDB(id="3", bookName="So Not The Drama",
               authorName="Paula Chase",
               coverUrl="bla bla",
               description="...", category="Fiction", user_id=1)

session.add(book3)
session.commit()

book4 = BookDB(id="4", bookName="This Blue Novel",
               authorName="Valerie Mejer Caso",
               coverUrl="bla bla",
               description="...", category="Mystery", user_id=1)

session.add(book4)
session.commit()
