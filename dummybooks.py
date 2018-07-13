from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BookDB, User, CategoryDB
import os

engine = create_engine('sqlite:///BookCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="admin", email="mahmoud.beshir94@gmail.com")
session.add(User1)
session.commit()

# Create categories

category1 = CategoryDB(id=1, name="Fantasy")

session.add(category1)
session.commit()

category2 = CategoryDB(id=1, name="Romance")

session.add(category2)
session.commit()

category3 = CategoryDB(id=1, name="Mystery")

session.add(category3)
session.commit()

category4 = CategoryDB(id=1, name="Fiction")

session.add(category4)
session.commit()

category5 = CategoryDB(id=1, name="Horror")

session.add(category5)
session.commit()

category6 = CategoryDB(id=1, name="Other")

session.add(category6)
session.commit()


# Create dummy books data
book1 = BookDB(bookName="Hello!",
               authorName="Janine Amos",
               coverUrl="bla bla",
               description="...", category="Other", user_id=1)

session.add(book1)
session.commit()

book2 = BookDB(bookName="Romantic Poetry, Volume 7",
               authorName="Angela Esterhammer",
               coverUrl="bla bla",
               description="...", category="Romance", user_id=1)

session.add(book2)
session.commit()

book3 = BookDB(bookName="So Not The Drama",
               authorName="Paula Chase",
               coverUrl="bla bla",
               description="...", category="Fiction", user_id=1)

session.add(book3)
session.commit()

book4 = BookDB(bookName="This Blue Novel",
               authorName="Valerie Mejer Caso",
               coverUrl="bla bla",
               description="...", category="Mystery", user_id=1)

session.add(book4)
session.commit()