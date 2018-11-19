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

#spotify API
username = ""
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
spotify = SpotifyPlaylist.createSpotifyToken(token)

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'

headers = {'Accept': 'application/json', 'x-api-key': setCONSUMER_KEY}

print spotify
print 'Please enter how you wish to search for looking up the setlist'
print
selection = raw_input('Enter 1 for artist name, 2 for date, 3 for venue: ')
print

#Input search term type (artist, date, or city/venue)
if selection == '1':
    name = raw_input("Enter artist name: ")
    artistID = SearchSetlist.getArtistID(headers, name)
    spotArtist = SpotifyPlaylist.searchTermsArtist(spotify, name)
    print 'Setlist: '
    print artistID
    print SearchSetlist.getArtistSetlist(artistID, headers) #print data from setlist.fm
    print
    print 'Spotify: '
    print spotArtist
elif selection == '2':
    print('Enter the date.')
    month = raw_input('Enter the month: ')
    day = raw_input('Enter the day: ')
    year  = raw_input('Enter the year: ')
elif selection == '3':
    cityID = SearchSetlist.getCityID(headers)
    print cityID
    print SearchSetlist.getVenueSetlist(cityID, headers)
else:
    print('Not a valid input. Try again.')
