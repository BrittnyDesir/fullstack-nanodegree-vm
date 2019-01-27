from flask import Flask, render_template
from flask import request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from catalog_db_setup import Base, OutdoorActivity, Items, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(open('client_secrets.json', 'r').
                       read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Connect to Database
engine = create_engine('sqlite:///catalogwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Connect
@app.route('/gconnect', methods=['POST', 'GET'])
def gconnect():
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
        print "Token's client ID does not match app's."
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
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # login_session['username'] = data['name']
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
    output += '<h1>Welcome, '
    output += login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    flash("you are now logged in as %s" % login_session['email'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect', methods=['GET'])
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    # print 'User name is: '
    print login_session['email']
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        # del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions


def createUser(login_session):
    newUser = User(email=login_session[
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
    except:
        return None


# Route that returns activity and it's list of gear in JSON


@app.route('/gear/<int:activity_id>/list/JSON')
def outdoorActivityGearJSON(activity_id):
    activity = session.query(OutdoorActivity).filter_by(id=activity_id).one()
    items = session.query(Items).filter_by(activity_id=activity.id).all()
    return jsonify(Items=[i.serialize for i in items])


# Route that returns a particular item in JSON


@app.route('/gear/<int:activity_id>/list/<int:gear_id>/JSON')
def gearItemJSON(activity_id, gear_id):
    gearItem = session.query(Items).filter_by(id=gear_id).one()
    return jsonify(Items=gearItem.serialize)


# Route that returns the list of activities in JSON


@app.route('/activities/JSON')
def activityListJSON():
    activities = session.query(OutdoorActivity).all()
    return jsonify(activities=[i.serialize for i in activities])


# Show all activities

@app.route('/')
@app.route('/activities/home')
def outdoorActivities():
    activity = session.query(
        OutdoorActivity).order_by(asc(OutdoorActivity.name))
    return render_template('activities.html', activity=activity)


# Create New Activity


@app.route('/activity/add/', methods=['GET', 'POST'])
def newActivity():
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newActivity = OutdoorActivity(name=request.form['name'],
                                      user_id=login_session['user_id'])
        session.add(newActivity)
        session.commit()
        flash("New Activity Added!")
        return redirect(url_for('outdoorActivities'))
    else:
        return render_template('newactivity.html')


# Edit Activity


@app.route('/activity/<int:activity_id>/edit/', methods=['GET', 'POST'])
def editActivity(activity_id):
    editedActivity = (session.query(OutdoorActivity).
                      filter_by(id=activity_id).one())
    if 'email' not in login_session:
        return redirect('/login')
    if editedActivity.user_id != login_session['user_id']:
        flash('Not authorized to perform this action!')
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedActivity.name = request.form['name']
            flash('Activity Edited Successfully')
            return redirect(url_for('outdoorActivities'))
    else:
        return render_template('editactivity.html', activity=editedActivity)


# Delete an Activity


@app.route('/activity/<int:activity_id>/delete/', methods=['GET', 'POST'])
def deleteActivity(activity_id):
    activityToDelete = (session.query(OutdoorActivity).
                        filter_by(id=activity_id).one())
    if 'email' not in login_session:
        return redirect('/login')
    if activityToDelete.user_id != login_session['user_id']:
        flash('Not authorized to perform this action!')
        return redirect('/login')
    if request.method == 'POST':
        session.delete(activityToDelete)
        flash('Successfully Deleted Activity')
        session.commit()
        return redirect(url_for('outdoorActivities', activity_id=activity_id))
    else:
        return render_template('deleteactivity.html',
                               activity=activityToDelete)


# View Activity Gear


@app.route('/gear/<int:activity_id>')
def outdoorActivityGear(activity_id):
    activity = session.query(OutdoorActivity).filter_by(id=activity_id).one()
    items = session.query(Items).filter_by(activity_id=activity.id).all()
    return render_template('catalog.html', items=items, activity=activity)


# Add New Gear to Activity


@app.route('/gear/<int:activity_id>/add/', methods=['GET', 'POST'])
def newGear(activity_id):
    if 'email' not in login_session:
        return redirect('/login')
    activity = session.query(OutdoorActivity).filter_by(id=activity_id).one()
    if login_session['user_id'] != activity.user_id:
        flash('Not authorized to perform this action!')
        return redirect('/login')
    if request.method == 'POST':
        newItem = Items(name=request.form['name'], price=request.form['price'],
                        description=request.form['description'],
                        user_id=activity.user_id, activity_id=activity_id)
        session.add(newItem)
        session.commit()
        flash("New Gear Added!")
        return redirect(url_for('outdoorActivityGear',
                        activity_id=activity_id))
    else:
        return render_template('newgear.html', activity_id=activity_id)


# Edit Gear


@app.route('/gear/<int:activity_id>/<int:gear_id>/edit/',
           methods=['GET', 'POST'])
def editGear(activity_id, gear_id):
    if 'email' not in login_session:
        return redirect('/login')
    editedGear = session.query(Items).filter_by(id=gear_id).one()
    activity = session.query(OutdoorActivity).filter_by(id=activity_id).one()
    if login_session['user_id'] != activity.user_id:
        flash('Not authorized to perform this action!')
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editedGear.name = request.form['name']
        if request.form['price']:
            editedGear.price = request.form['price']
        if request.form['description']:
            editedGear.description = request.form['description']
        session.add(editedGear)
        session.commit()
        flash("Gear Has Been Edited")
        return redirect(url_for('outdoorActivityGear',
                                activity_id=activity_id))
    else:
        return render_template('editgear.html',
                               activity_id=activity_id,
                               gear_id=gear_id, item=editedGear)


# Delete Gear


@app.route('/gear/<int:activity_id>/<int:gear_id>/delete/',
           methods=['GET', 'POST'])
def deleteGear(activity_id, gear_id):
    if 'email' not in login_session:
        return redirect('/login')
    gearToDelete = session.query(Items).filter_by(id=gear_id).one()
    activity = session.query(OutdoorActivity).filter_by(id=activity_id).one()
    if login_session['user_id'] != activity.user_id:
        flash('Not authorized to perform this action!')
        return redirect('/login')
    if request.method == 'POST':
        session.delete(gearToDelete)
        session.commit()
        flash("Gear Has Been Deleted")
        return redirect(url_for('outdoorActivityGear',
                                activity_id=activity_id))
    else:
        return render_template('deletegear.html', item=gearToDelete)


if __name__ == '__main__':
    app.secret_key = 'some_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
