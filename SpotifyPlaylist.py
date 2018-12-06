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

def searchTracks(spotify, artistName, trackName):
    trackList = []
    search = spotify.search(q= artistName + " " + trackName, type="track")
    for i, t in enumerate(search['tracks']['items']):
        tracks = (t['uri'])
        if i == 0:
            trackList.append(tracks)
    return trackList

def createTrackList(spotify, username, artistName, setlist):
    trackIds = []
    for i in setlist:
        trackID = searchTracks(spotify, artistName, i)
        trackIds.append(trackID)
    return trackIds

def addTrackList(spotify, username, playlistID, trackIDs):
    for trackID in trackIDs:
        spotify.user_playlist_add_tracks(username, playlistID, trackID, position=None)
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
            return playlist['uri']
