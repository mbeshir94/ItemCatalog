#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, BookDB, User, CategoryDB
import random
import string
import httplib2
import json
import requests
import logging
from oauth2client.client import AccessTokenCredentials
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy.pool import SingletonThreadPool

handler = logging.FileHandler('app.log')  # errors logged to this file
handler.setLevel(logging.ERROR)  # only log errors and above

app = Flask(__name__)
app.secret_key = 'itsasecret'
app.logger.addHandler(handler)

# google client secret
secret_file = json.loads(open('client_secret.json', 'r').read())
CLIENT_ID = secret_file['web']['client_id']
APPLICATION_NAME = 'BooksCatalog'

engine = create_engine('postgresql://postgres:postgres@localhost/BookCatalog')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine, autoflush=True))
session = DBSession()


# validate signed in user

def check_user():
    email = login_session['email']
    return session.query(User).filter_by(email=email).one_or_none()

def check_admin():
    return session.query(User).filter_by(
        email='mahmoud.beshir94@gmail.com').one_or_none()


# Create new user and add it to database

def createUser():
    name = login_session['name']
    email = login_session['email']
    url = login_session['img']
    provider = login_session['provider']
    newUser = User(name=name, email=email, image=url, provider=provider)
    try:
        session.add(newUser)
        session.commit()
    except:
        session.rollback()
        raise


def new_state():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in xrange(32))
    login_session['state'] = state
    return state


def queryAllBooks():
    return session.query(BookDB).all()

@app.route('/')
@app.route('/books/')
def showBooks():
    categories = session.query(CategoryDB).all()
    books = queryAllBooks()
    state = new_state()
    return render_template('main.html', categories=categories, books=books, currentPage='main',
                           state=state, login_session=login_session)

# add new book

@app.route('/book/new/', methods=['GET', 'POST'])
def newBook():
    categories = session.query(CategoryDB).all()
    if request.method == 'POST':

        # check if user is logged in or not

        if 'provider' in login_session and \
                    login_session['provider'] != 'null':
            bookName = request.form['bookName']
            bookAuthor = request.form['authorName']
            coverUrl = request.form['bookImage']
            description = request.form['bookDescription']
            description = description.replace('\n', '<br>')
            bookCategory = request.form['category']
            user_id = check_user().id

            if bookName and bookAuthor and coverUrl and description \
                    and bookCategory:
                newBook = BookDB(
                    bookName=bookName,
                    authorName=bookAuthor,
                    coverUrl=coverUrl,
                    description=description,
                    category=bookCategory,
                    user_id=user_id,
                    )
                session.add(newBook)
                session.commit()
                return redirect(url_for('showBooks'))
            else:
                state = new_state()
                return render_template(
                    'newItem.html',
                    currentPage='new',
                    categories = categories,
                    title='Add New Book',
                    errorMsg='All Fields are Required!',
                    state=state,
                    login_session=login_session,
                    )
        else:
            state = new_state()
            books = queryAllBooks()
            return render_template(
                'main.html',
                books=books,
                currentPage='main',
                state=state,
                login_session=login_session,
                errorMsg='Please Login first to Add Book!',
                )
    elif 'provider' in login_session and login_session['provider'] \
            != 'null':
        state = new_state()
        return render_template('newItem.html', categories = categories, currentPage='new',
                               title='Add New Book', state=state,
                               login_session=login_session)
    else:
        state = new_state()
        books = queryAllBooks()
        return render_template(
            'main.html',
            books=books,
            currentPage='main',
            state=state,
            login_session=login_session,
            errorMsg='Login first!',
            )


# show book of different category

@app.route('/books/category/<string:category>/')
def sortBooks(category):
    categories = session.query(CategoryDB).all()
    books = session.query(BookDB).filter_by(category=category).all()
    state = new_state()
    return render_template(
        'main.html',
        books=books,
        categories=categories,
        currentPage='main',
        error='No Books With This Genre!',
        state=state,
        login_session=login_session)


# show book data

@app.route('/books/category/<string:category>/<int:bookId>/')
def bookDetail(category, bookId):
    categories = session.query(CategoryDB).all()
    book = session.query(BookDB).filter_by(id=bookId,
                                           category=category).first()
    state = new_state()
    if book:
        return render_template('itemDetail.html', book=book,
                               categories=categories,
                               currentPage='detail', state=state,
                               login_session=login_session)
    else:
        return render_template('main.html', currentPage='main',
                               categories=categories,
                               error="""No Book Found with this Category
                               and Book Id :(""",
                               state=state,
                               login_session=login_session)


# edit book data

@app.route('/books/category/<string:category>/<int:bookId>/edit/',
           methods=['GET', 'POST'])
def editBookDetails(category, bookId):
    book = session.query(BookDB).filter_by(id=bookId,
                                           category=category).first()
    categories = session.query(CategoryDB).all()
    if request.method == 'POST':

        # check if the user is signed in

        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            bookName = request.form['bookName']
            bookAuthor = request.form['authorName']
            coverUrl = request.form['bookImage']
            description = request.form['bookDescription']
            bookCategory = request.form['category']
            user_id = check_user().id
            admin_id = check_admin().id

            # check if the signed in user is the owner

            if book.user_id == user_id or user_id == admin_id:
                if bookName and bookAuthor and coverUrl and description \
                        and bookCategory:
                    book.bookName = bookName
                    book.authorName = bookAuthor
                    book.coverUrl = coverUrl
                    description = description.replace('\n', '<br>')
                    book.description = description
                    book.category = bookCategory
                    session.add(book)
                    session.commit()
                    return redirect(url_for('bookDetail',
                                    category=book.category,
                                    categories=categories,
                                    bookId=book.id))
                else:
                    state = new_state()
                    return render_template(
                        'editItem.html',
                        currentPage='edit',
                        title='Edit Book Details',
                        book=book,
                        categories = categories,
                        state=state,
                        login_session=login_session,
                        errorMsg='All Fields are Required!',
                        )
            else:
                state = new_state()
                return render_template(
                    'itemDetail.html',
                    book=book,
                    categories=categories,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Only Owner can Edit the Book Data')
        else:
            state = new_state()
            return render_template(
                'itemDetail.html',
                book=book,
                categories=categories,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login First to Edit the Book Data',
                )
    elif book:
        state = new_state()
        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            user_id = check_user().id
            admin_id = check_admin().id
            if user_id == book.user_id or user_id == admin_id:
                book.description = book.description.replace('<br>', '\n')
                return render_template(
                    'editItem.html',
                    currentPage='edit',
                    title='Edit Book Details',
                    book=book,
                    categories = categories,
                    state=state,
                    login_session=login_session,
                    )
            else:
                return render_template(
                    'itemDetail.html',
                    book=book,
                    categories=categories,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Only Owner can Edit the Book Data')
        else:
            return render_template(
                'itemDetail.html',
                book=book,
                categories=categories,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Edit the Book Details!',
                )
    else:
        state = new_state()
        return render_template('main.html', currentPage='main',
                               error="""No Book Found
                               with this Category and Book Id!""",
                               state=state,
                               login_session=login_session)


# delete books

@app.route('/books/category/<string:category>/<int:bookId>/delete/')
def deleteBook(category, bookId):
    categories = session.query(CategoryDB).all()
    book = session.query(BookDB).filter_by(category=category,
                                           id=bookId).first()
    state = new_state()
    if book:

        # check if user is logged in or not

        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            user_id = check_user().id
            admin_id = check_admin().id
            if user_id == book.user_id or user_id == admin_id:
                session.delete(book)
                session.commit()
                return redirect(url_for('showBooks'))
            else:
                return render_template(
                    'itemDetail.html',
                    book=book,
                    categories=categories,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Only the Owner Can delete the book'
                    )
        else:
            return render_template(
                'itemDetail.html',
                book=book,
                categories=categories,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Delete the Book!',
                )
    else:
        return render_template('main.html', currentPage='main',
                               error="""No Book Found
                               with this Category and Book Id :(""",
                               state=state,
                               login_session=login_session)


@app.route('/books.json/')
def booksJSON():
    books = session.query(BookDB).all()
    return jsonify(Books=[book.serialize for book in books])


@app.route('/books/category/<string:category>.json/')
def bookCategoryJSON(category):
    books = session.query(BookDB).filter_by(category=category).all()
    return jsonify(Books=[book.serialize for book in books])


@app.route('/books/category/<string:category>/<int:bookId>.json/')
def bookJSON(category, bookId):
    book = session.query(BookDB).filter_by(category=category,
                                           id=bookId).first()
    return jsonify(Book=book.serialize)


# google signin function

@app.route('/gconnect', methods=['POST'])
def gConnect():
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:

        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade the
        authorisation code"""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                            """Token's user ID does not
                            match given user ID."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = access_token
    login_session['id'] = gplus_id

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['name'] = data['name']
    login_session['img'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    if not check_user():
        createUser()
    return jsonify(name=login_session['name'],
                   email=login_session['email'],
                   img=login_session['img'])


# logout user

@app.route('/logout', methods=['post'])
def logout():

    if login_session.get('provider') == 'google':
        return gdisconnect()
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']

    if access_token is None:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    header = httplib2.Http()
    result = header.request(url, 'GET')[0]

    if result['status'] == '200':

        del login_session['credentials']
        del login_session['id']
        del login_session['name']
        del login_session['email']
        del login_session['img']
        login_session['provider'] = 'null'
        response = make_response(json.dumps({'state': 'loggedOut'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        response = make_response(json.dumps({'state': 'errorRevoke'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.run()
