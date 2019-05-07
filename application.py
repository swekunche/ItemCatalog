#! /usr/bin/env python2.7

from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from flask import session as login_session
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database_setup import Base, Category, Item
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import logging

CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine(
    'sqlite:///ItemCatalog1.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Begin Authorization code


@app.route('/login/')
def LoginFunction():
    """Login route
    """
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Google authentication connect
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Put Auth code into object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        logging.debug("About to get 401 error")
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        logging.debug("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    logging.debug("Login access_token:"+credentials.access_token)
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """style = "width: 300px; height: 300px;border-radius: 150px;
                -webkit-border-radius: 150px;-moz-border-radius: 150px;">"""
    flash("you are now logged in as %s" % login_session['username'])
    logging.debug("done!")
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Google authentication disconnect
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    logging.debug('In gdisconnect access token is %s', access_token)
    url = 'https://accounts.google.com/o/oauth2/revoke'
    revoke = requests.post(url, params={'token': access_token},
                           headers={'content-type':
                                    'application/x-www-form-urlencoded'})
    result = getattr(revoke, 'status_code')
    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Disconnected.'), 200)
        flash("You have Successfully logged out")
        redirect('/Catalog')
    return redirect('/Catalog')

# JSON APIs to view Catalog Information
@app.route('/Catalog/categories/JSON')
def categoriesJSON():
    """JSON API for categories
    """
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


@app.route('/Catalog/latestItems/JSON')
def latestItemsJSON():
    """JSON API for latest items
    """
    latestItems = session.query(Item).order_by('created_date').limit(10)
    return jsonify(latestItems=[i.serialize for i in latestItems])


@app.route('/Catalog/<string:category_name>/items/JSON')
def itemsinCategory(category_name):
    """JSON API for items in category
    """
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(items=[i.serialize for i in items])

# Show all Categories
@app.route('/')
@app.route('/Catalog')
def showCategories():
    """To show categories of items
    """
    if 'username' not in login_session:
        return redirect('/login')
    else:
        categories = session.query(Category).all()
        latestItems = session.query(Item).order_by('created_date').limit(10)
        return render_template('categories.html',
                               categories=categories, latestItems=latestItems)

# Show all items in a Category
@app.route('/Catalog/<string:category_name>/items/')
def showItems(category_name):
    """To show items in category
    """
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('items.html', categories=categories,
                           items=items, category=category)

# create a new item
@app.route('/Catalog/new/', methods=['GET', 'POST'])
def createItem():
    """To create item in a category
    """
    if request.method == 'POST':
        category_id = request.form['category']
        category = session.query(Category).filter_by(id=category_id).one()
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       category_id=request.form['category'],
                       username=login_session['username'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.title)
        session.commit()
        return redirect(url_for('showItems', category_name=category.name))
    else:
        categories = session.query(Category).all()
        return render_template('newitem.html', categories=categories)

# Show an item
@app.route('/Catalog/<string:category_name>/<string:item_name>')
@app.route('/Catalog/<string:item_name>')
def showItem(item_name):
    """To show item details
    """
    item = session.query(Item).filter_by(title=item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if item.username != login_session['username']:
        category = session.query(Category).filter_by(id=item.category_id).one()
        return render_template('showitem.html', category=category,
                               item_name=item_name, item=item, showLinks=False)
    else:
        category = session.query(Category).filter_by(id=item.category_id).one()
        return render_template('showitem.html', category=category,
                               item_name=item_name, item=item, showLinks=True)

# Edit an item
@app.route('/Catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    """To show item to edit and update details
    """
    item = session.query(Item).filter_by(title=item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if item.username != login_session['username']:
        return """<script>function myFunction()
         {alert('You are not authorized to edit this item.
         Please create your own item in order to edit.');}
        </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        category = session.query(Category).filter_by(name=category_name).one()
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category_id = request.form['category']
        session.add(item)
        session.commit()
        flash('Item Successfully Edited %s' % item.title)
        return render_template('showitem.html', category=category,
                               item_id=item_name, item=item, showLinks=True)
    else:
        categories = session.query(Category).all()
        return render_template('edititem.html', categories=categories,
                               item_id=item_name, item=item)

# Delete an item
@app.route('/Catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    """to delete the item
    """
    itemToDelete = session.query(Item).filter_by(title=item_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.username != login_session['username']:
        return """<script>function myFunction() {alert('You
         are not authorized to delete this item. Please create
          your own item in order to delete.');}
          </script><body onload='myFunction()'>"""
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.title)
        session.commit()
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template('deleteItem.html',
                               item=itemToDelete, category=category)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
