from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import Credentials
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalogmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """ Create anti-forgery state token and show the login page """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Request an access token from the Google Authorization Server,
    extract a token from the response, and send the token to the
    Google+ API
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json()
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h3 class = "text-center">Welcome, '
    output += login_session['username']
    output += '!</h3></br>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    print output
    return output


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """ Provide Facebook login for user """
    if request.args.get('state') != login_session['state']:
        response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s'\
        % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.2/me?%s' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    # let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200'\
        % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2 class = "text-center">Welcome, '
    output += login_session['username']
    output += '!</h2></br>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; \
               border-radius: 150px; -webkit-border-radius: 150px; \
               -moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """ Disconnect user from Facebook """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s?%s/permissions' % \
        (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


def createUser(login_session):
    """ Reture the new user's id
    If user does not exist in the datase, add this new user to the database.
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """ Get user information through user id from database """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """ Get user's id through given email from database  """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """ Disconnect from Goole+ API
    Revoke a current user's token and reset their login_session
    """
    # Only disconnect a connected user.
    #credentials = login_session.get('credentials').from_json()
    credentials = Credentials.new_from_json(login_session.get('credentials'));
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/JSON')
def catalogJSON():
    """ JSON APIs to view Catalog Information """
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])


@app.route('/catalog/<int:catalog_id>/JSON')
def catalogItemJSON(catalog_id):
    """ JSON APIs to view catalog items Information """
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(
            catalog_id=catalog_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/')
@app.route('/catalog')
def catalogMenu():
    """ Show all catalogs and latest added items """
    catalogs = session.query(Catalog).all()
    latestItems = session.query(CatalogItem).order_by(CatalogItem.id)[:-10:-1]
    if 'username' not in login_session:
        return render_template(
            'publicCatalog.html', catalogs=catalogs, latestItems=latestItems)
    else:
        return render_template(
            'catalog.html', catalogs=catalogs, latestItems=latestItems)


@app.route('/')
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCatalog():
    """ Create a new catalog and add the new catalog to database """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id']
        )
        session.add(newCatalog)
        session.commit()
        flash("New catalog %s is added" % newCatalog.name)
        return redirect(url_for('catalogMenu'))
    else:
        return render_template('newCatalog.html')


@app.route('/')
@app.route('/catalog/<int:catalog_id>')
def catalogItems(catalog_id):
    """ Show all the items for catalog """
    catalogs = session.query(Catalog).all()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(
            catalog_id=catalog_id).all()
    creator = getUserInfo(catalog.user_id)

    if 'username' not in login_session:
        return render_template(
            'publicCatalogItem.html', catalogs=catalogs, catalog=catalog,
            catalog_id=catalog_id, items=items, ceator=creator)
    else:
        return render_template(
            'catalogitem.html', catalog=catalog, items=items,
            catalog_id=catalog_id, catalogs=catalogs, creator=creator)


@app.route('/')
@app.route('/catalog/<int:catalog_id>/new', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
    """ Create a new catalog item and add the item to database """
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() { \
            alert('You are not authorized to add new item to this catalog.\
                Please create your own catalog in order to add items.');\
            window.location.href='/catalog';}\
            </script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = CatalogItem(
            name=request.form['name'], description=request.form['description'],
            catalog_id=catalog_id, user_id=catalog.user_id)
        session.add(newItem)
        session.commit()
        flash("New catalog item %s is added" % newItem.name)
        return redirect(url_for('catalogItems', catalog_id=catalog_id))
    else:
        return render_template('newCatalogItem.html', catalog_id=catalog_id)


@app.route('/')
@app.route('/catalog/<int:catalog_id>/edit',
           methods=['GET', 'POST'])
def editCatalog(catalog_id):
    """ Edit information about a catalog """
    if 'username' not in login_session:
        return redirect('/login')
    editedCatalog = session.query(Catalog).filter_by(id=catalog_id).one()

    if login_session['user_id'] != editedCatalog.user_id:
        return "<script>function myFunction() {\
                alert('You are not authorized to edit this catalog. \
                You can only edit your own catalogs.');\
                window.location.href='/catalog';}\
                </script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedCatalog.name = request.form['name']
        if request.form['description']:
            editedCatalog.description = request.form['description']
        session.add(editedCatalog)
        session.commit()
        flash("Catalog %s is edited" % editedCatalog.name)
        return redirect(url_for('catalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'editcatalog.html', editedCatalog=editedCatalog)


@app.route('/')
@app.route('/catalog/<int:catalog_id>/delete', methods=['GET', 'POST'])
def deleteCatalog(catalog_id):
    """ Delete a specific catalog from database """
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    itemsToDelete = session.query(CatalogItem).filter_by(
                catalog_id=catalog_id).all()
    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() { \
                alert('You are not authorized to delete this catalog.');\
                window.location.href='/catalog';}\
                </script><body onload='myFunction()''>"

    if request.method == 'POST':
        for item in itemsToDelete:
            session.delete(item)
        session.delete(catalog)
        session.commit()
        flash("Catalog %s is Deleted" % catalog.name)
        return redirect(url_for('catalogMenu'))
    else:
        return render_template(
            'deletecatalog.html', catalog_id=catalog_id, catalog=catalog)


@app.route('/')
@app.route('/catalog/<int:catalog_id>/<int:catalogItem_id>')
def showItemInfo(catalog_id, catalogItem_id):
    """ Show information about the catalog item """
    item = session.query(CatalogItem).filter_by(id=catalogItem_id).one()
    if 'username' not in login_session:
        return render_template(
            'publiciteminfo.html', catalogItem_id=catalogItem_id, item=item)
    else:
        return render_template(
            'showiteminfo.html', catalogItem_id=catalogItem_id, item=item)


@app.route('/')
@app.route('/catalog/<int:catalog_id>/<int:catalogItem_id>/edit',
           methods=['GET', 'POST'])
def editCatalogItem(catalog_id, catalogItem_id):
    """ Edit information about a catalog item """
    if 'username' not in login_session:
        return redirect('/login')
    catalogs = session.query(Catalog).all()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    editedItem = session.query(CatalogItem).filter_by(
                    id=catalogItem_id).one()

    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() {\
                alert('You are not authorized to edit this catalog item. \
                You can only edit your own catalog item.');\
                window.location.href='/catalog';}\
                </script><body onload='myFunction()''>"

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        requestedCatalog = session.query(Catalog).filter_by(
            id=request.form['catalogID']).one()
        if request.form['catalogID'] and \
           login_session['user_id'] != requestedCatalog.user_id:
            return "<script>function myFunction() {\
                alert('You are not authorized to add items to this catalog. \
                Please put this item in your own catalogs.');\
                window.location.href='/catalog';}\
                </script><body onload='myFunction()''>"

        if request.form['catalogID']:
            editedItem.catalog_id = request.form['catalogID']
        session.add(editedItem)
        session.commit()
        flash("Catalog Item %s is edited" % editedItem.name)
        return redirect(url_for('catalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'editcatalogitem.html', catalog=catalog,
            catalogItem_id=catalogItem_id, item=editedItem, catalogs=catalogs)


@app.route('/')
@app.route('/catalog/<int:catalog_id>/<int:catalogItem_id>/delete',
           methods=['GET', 'POST'])
def deleteCatalogItem(catalog_id, catalogItem_id):
    """ Delete a catalog item from database """
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    itemToDelete = session.query(CatalogItem).filter_by(
                id=catalogItem_id).one()

    if login_session['user_id'] != catalog.user_id:
        return "<script>function myFunction() {\
                alert('You are not authorized to delete catalog items \
                    in this catalog.');\
                window.location.href='/catalog';}\
                </script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Catalog Item %s is Deleted" % itemToDelete.name)
        return redirect(url_for('catalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'deletecatalogitem.html', catalog_id=catalog_id, item=itemToDelete)


@app.route('/disconnect')
def disconnect():
    """ Disconnect based on provider """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('catalogMenu'))
    else:
        flash("You were not logged in")
        return redirect(url_for('catalogMenu'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
