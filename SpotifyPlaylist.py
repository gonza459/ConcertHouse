import pprint
import sys

import spotipy
import spotipy.util as util
import spotipy.client as client
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import json

spotify = spotipy.Spotify()
tracks = []

#spotify API
spotCONSUMER_KEY = '3817588cd345435c86c9a60e6c0cb70a'
spotCONSUMER_SECRET = 'ce6c55f9f3c343bb919d917257661a3b'
spotREDIRECT_URI = 'SpotifyTestApp://callback'

username = "1256796696"
token = util.prompt_for_user_token(
    username,
    scope = 'playlist-modify-private playlist-modify-public',
    #Enter Spotify API ID
    client_id ='3817588cd345435c86c9a60e6c0cb70a',
    #Enter Spotify API Secret
    client_secret ='ce6c55f9f3c343bb919d917257661a3b',
    #Enter Spotify API Redirect URI
    redirect_uri='SpotifyTestApp://callback'
)

#Create a session token for spotipy
def createSpotifyToken(token):
    spotify = spotipy.Spotify(auth=token)
    return spotify

def createSpotifyPlaylsit(username, playlistName, playlistDescription):
    playlists = spotify.user_playlist_create(username, playlistName,
                                        playlistDescription)
    return pprint.pprint(playlists)

def searchTermsArtist(spotify, artistName):
    results = spotify.search(q='' + artistName, type='artist')
    return results
