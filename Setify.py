import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import os
import json

import SpotifyPlaylist
import SearchSetlist

set = []

#spotify API
username = "1256796696"
token = util.prompt_for_user_token(
    username,
    scope = 'playlist-modify-private playlist-modify-public',
    #Enter Spotify API ID
    client_id ='3817588cd345435c86c9a60e6c0cb70a',
    #Enter Spotify API Secret
    client_secret ='ce6c55f9f3c343bb919d917257661a3b',
    #Enter Spotify API Redirect URI
    redirect_uri='http://localhost/'
)
#create session token for spotify
spotify = SpotifyPlaylist.createSpotifyToken(token)

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'

headers = {'Accept': 'application/json', 'x-api-key': setCONSUMER_KEY}

print spotify
print 'Please enter how you wish to search for looking up the setlist'
selection = ''
print
while selection != '1' or '2':
    selection = raw_input('Enter 1 for artist name or 2 for venue: ')

    #Input search term type (artist, or city/venue)
    if selection == '1':
        name = raw_input("Enter artist name: ")
        #Searches setlist.fm data for artist mbid
        artistID = SearchSetlist.getArtistID(headers, name)
        #searches spotify data for info relating to artist name
        spotArtist = SpotifyPlaylist.searchTermsArtist(spotify, name)
        print 'Setlist: '
        print artistID
        print SearchSetlist.getArtistSetlist(artistID, headers) #print data from setlist.fm
        print
        print 'Spotify: '
        print spotArtist
        playlistName = 'test'
        playlistDescription = 'test'
        playlist = spotify.user_playlist_create(username, playlistName, playlistDescription)
        pprint.pprint(playlist)
        break

    #takes in year
    #elif selection == '2':
    #    print('Enter the year')

    #Search for most recent setlist according to venue name
    elif selection == '2':
        venue = raw_input('Enter the venue name: ')
        #searches setlit.fm data for venue id
        cityID = SearchSetlist.getVenueID(headers, venue)
        #print venue ID
        print cityID
        print SearchSetlist.getVenueSetlist(cityID, headers)
        break

    else:
        print('Not a valid input. Try again.')
