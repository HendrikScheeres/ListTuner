'''
ListTuner - Hendrik Scheeres
spotify.py

This is main Flask application of the ListTuner website.
 '''

import os
import requests
import json

from authlib.integrations.flask_client import OAuth

from flask import Flask, session, render_template, request, url_for, redirect, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *

from spotify import *

# configure Flask app
app = Flask(__name__)

# configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# configure session, use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure migrations
Migrate(app, db)

# configuer OAuth
if not os.getenv("CLIENT_ID") or not os.getenv("CLIENT_SECRET"):
    raise RuntimeError("CLIENT_ID and/or CLIENT_SECRET are/is not set")

# register the spotify API to OAuth
oauth = OAuth(app)
spotify = oauth.register(
    name = 'spotify',
    client_id = os.getenv("ClIENT_ID"),
    client_secret = os.getenv("ClIENT_SECRET"),
    access_token_url = 'https://accounts.spotify.com/api/token',
    access_token_params = None,
    authorize_url = 'https://accounts.spotify.com/authorize',
    authorize_params = None,
    api_base_url = 'https://api.spotify.com/v1',
    client_kwargs = {'scope': 'user-read-private playlist-read-private playlist-read-collaborative'}
)


@app.route("/")
def frontpage():
    ''' Fronpage of the website '''

    return render_template("frontpage.html")


@app.route("/login")
def login():
    ''' Pathway that lets the user log into Spotify '''

    # create a Spotify client
    spotify = oauth.create_client('spotify')

    # set the redirect uri
    redirect_uri = url_for('authorize', _external=True)

    # redirect to the Spotify login page and request the access token
    return spotify.authorize_redirect(redirect_uri)


@app.route("/logout")
def logout():
    ''' Logs the user out '''

    # check if a user is logged in
    if "token" not in session:
        return redirect(url_for("frontpage"))

    # remove all session keys
    for key in list(session.keys()):
        session.pop(key)

    return redirect(url_for("frontpage"))


@app.route('/authorize')
def authorize():
    ''' Authorizes the acces token and creates user session '''

    # create the client and request the access token
    spotify = oauth.create_client('spotify')
    token = spotify.authorize_access_token()

    # format the authorization dict to make api requests
    headers = {
    "Authorization": token["token_type"] + " " + token["access_token"]
    }

    # save the token and profile in the session
    session['token'] = token
    session['headers'] = headers

    return redirect('/playlists')


@app.route("/playlists")
def playlistspage():
    ''' Page with the overview of the users playlists '''

    # check if a user is logged in
    if "token" not in session:
        return redirect(url_for("frontpage"))

    # get the user info
    headers = session["headers"]

    try:
        user_info = get_user_info(headers=headers)
    except Exception as e:
        return render_template("error.html", message=e)

    return render_template("playlistspage.html", user_info=user_info)


@app.route("/statistics:<string:id>")
def statisticspage(id):
    ''' Page with overview of the playlist statistics '''

    # check if a user is logged in
    if "token" not in session:
        return redirect(url_for("frontpage"))

    # get the playlist info
    headers = session["headers"]

    try:
        playlist = get_playlist_info(id=id, headers=headers)
    except Exception as e:
        return render_template("error.html", message=e)

    # get seals playlist info from database
    seals = Seals.query.all()

    return render_template("statisticspage.html", playlist=playlist, seals=seals)


@app.route("/statistics", methods=["POST"])
def statistics():
    ''' Requests playlist id from the statistics page and sends back playlist data '''

    # check if a user is logged in
    if "token" not in session:
        return redirect(url_for("frontpage"))

    # query for track_info
    playlist_id = request.form.get("playlist_id")

    headers = session["headers"]

    # get playlist track features
    try:
        track_features = get_track_features(playlist_id=playlist_id, headers=headers)
    except:
        return jsonify({"success": False})

    # get seal playlist track features
    try:
        seal_features = get_seal_features(headers=headers)
    except:
        return jsonify({"success": False})


    return jsonify({"success": True, "track_features": track_features, "seal_features": seal_features })
