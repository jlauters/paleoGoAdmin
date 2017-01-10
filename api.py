import json
import requests
import collections
import datetime
import time
import logging
from passlib.apps import custom_app_context as pwd_context
from functools import wraps, update_wrapper
from flask import Flask, request, current_app, make_response, session, escape, Response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import safe_str_cmp
from simpleCrossDomain import crossdomain
from basicAuth import check_auth, requires_auth

config = json.load(open('./config.json'));

# init
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = config['auth_secret']

# JWT
jwt = JWTManager(app)

# Core Routes
@app.route("/")
def index():

  resp = (("status", "ok"),
          ("msg", "paleoGo Admin API"))
  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

# Login
@app.route('/login', methods=['POST'])
@crossdomain(origin='*')
def login():

  username = request.form.get('username')
  password = request.form.get('password')
 
  # get User from DB
  if username is not None and password is not None:
    # Lookup user by username
    if pwd_context.verify(password, db_user['password']):

      ret = {'access_token': create_access_token(identity=username), 'user_id': db_user['user_id']}
      return Response(response=json.dumps(ret), status=200, mimetype="application/json")
  else:

    resp = (("status", "err"),
            ("msg", "username and password are required"))
    resp = collections.OrderedDict(resp)
    return Response(response=json.dumps(resp), status=200, mimetype="application/json")

# Logout
@app.route('/logout')
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def logout():
  db_session.pop('username', None)

# places
@app.route('/places', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def listPlaces():

  places = []
  #db Call get places

  resp = (("status", "ok"),
          ("places", places))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/places/add', methods=['POST'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def addPlace():

  name = request.form.get('name')

  #db call add place

  resp = (("status", "ok"),
          ("msg", "New place added"))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/places/<place_id>/delete', methods=['POST'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def removePlace(place_id):

  # db delete place
  resp = (("status", "ok"),
          ("msg", "place deleted"))
  
  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

# specimens
@app.route('/specimens/', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def listSpecimens():

  specimens = []
  # DB call get all specimens
  resp = (("status", "ok"),
          ("specimens", specimens))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/specimens/by_place/<place_id>', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def listPlaceSpecimens(place_id):

  place_specimens = []
  #DB call get specimens for place_id
  resp = (("status", "ok"),
          ("specimens", place_specimens))
  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/specimens/add', methods=['POST'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def addSpecimen():

  place_id = request.form.get('place_id')
  name     = request.form.get('name')
  lat      = request.form.get('lat')
  lng      = request.form.get('lng')

  specimen = {}
  #DB call Add Specimen
  resp = (("status", "ok"),
          ("msg", "specimen added successfully"),
          ("specimen", specimen))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/specimens/<specimen_id>', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def getSpecimen(specimen_id):

  specimen = {}
  #DB Call get specimen
  
  resp = (("status", "ok"),
          ("specimen", specimen))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/specimens/edit/<specimen_id>', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@jwt_required
def editSpecimen(specimen_id):

  place_id = request.form.get('place_id')
  name     = request.form.get('name')
  lat      = request.form.get('lat')
  lng      = request.form.get('lng')

  specimen = {}
  #DB call edit Specimen
  resp = (("status", "ok"),
          ("msg", "specimen edited successfully"),
          ("specimen", specimen))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=200, mimetype="application/json")


@app.errorhandler(404)
def page_not_found(e):

  resp = (("status", "err"),
          ("msg", "The request could not be completed"))

  resp = collections.OrderedDict(resp)
  return Response(response=json.dumps(resp), status=404, mimetype="application/json")

if __name__ == '__main__':
  app.run()
