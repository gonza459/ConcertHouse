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

token = util.prompt_for_user_token(
    username = "",
    scope = 'playlist-modify-private playlist-modify-public',
    #Enter Spotify API ID
    client_id ='3817588cd345435c86c9a60e6c0cb70a',
    #Enter Spotify API Secret
    client_secret ='ce6c55f9f3c343bb919d917257661a3b',
    #Enter Spotify API Redirect URI
    redirect_uri='http://spotify.com/us'
)

#Create a session token for spotipy
def createSpotifyToken(token):
    spotify = spotipy.Spotify(auth=token)
    return spotify

def searchTermsArtist(spotify, artistName):
    results = spotify.search(q='' + artistName, type='artist')
    return results

def searchTracks(spotify, trackName):
    results = spotify.search(q='' + trackName, type='track')
    return results

def createTrackList(spotify, username, playlistID, setlist):
    trackIDs = []
    #for track in setlist:
        #track.IDs.append(searchTracks(self, track))
    spotify.user_playlist_add_tracks(username, playlistID, trackIDs, position=None)
    return

def createSpotifyPlaylist(spotify, username, playlistName):
    public = True
    playlists = spotify.user_playlist_create(user=username, public= True, name=playlistName)
    return

def getSpotifyPlaylistID(spotify, username, playlistName):
    currentPlaylists = spotify.user_playlists(user=username)
    for playlist in currentPlaylists['items']:
        #Filter through the user's playlists to find the matching playlsit name
        if playlist['name'] == playlistName:
            return playlist['id']
