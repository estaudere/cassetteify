import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from flask import Flask, redirect, jsonify, request, render_template
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

SPOTIPY_CLIENT_ID=os.getenv('CLIENT_ID')
SPOTIPY_CLIENT_SECRET=os.getenv('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI="http://localhost:8000/callback"
SCOPE="user-top-read user-read-recently-played"

auth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE)
sp = spotipy.Spotify(auth_manager=auth)

@app.route('/')
def hello():
    return render_template('index.html')

    # cached_token = auth.get_cached_token()
    # if (cached_token):
    #     return cached_token
    # else:
    #     return "not logged in"

@app.route("/auth")
def authorize():
    return redirect(auth.get_authorize_url())

@app.route('/callback')
def callback():
    code = auth.parse_response_code(request.url)

    # once auth.get_access_token() is called, the token is stored in the cache
    # token_query contains access_token and refresh_token
    token_query = auth.get_access_token(code=code, check_cache=False)
    
    return redirect("/top_artists")

@app.route("/top_artists")
def top_artists():
    token_info = auth.get_cached_token()
    token = token_info['access_token']
    sp = spotipy.client.Spotify(auth=token)
    top_artists = sp.current_user_top_artists(limit=10, time_range='short_term')
    return render_template("cassettes.html", artists=top_artists)

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message))

    return dict(mdebug=print_in_console)

if __name__ == '__main__':
    app.run(host="localhost", port="8000", debug=True)
