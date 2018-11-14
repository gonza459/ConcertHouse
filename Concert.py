import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import os
import json

import PlaylistMaker

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
spotify = PlaylistMaker.createSpotifyToken(token)

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'

headers = {'Accept': 'application/json', 'x-api-key': setCONSUMER_KEY}

#Get the MusicBrainz ID for the artist
def getArtistID(header, name):
    #Replace any spaces with %20.
    artist = name.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/artists?artistName=" + artist + "&p=1&sort=relevance"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    for key in data['artist']:
        return key['mbid']

def getCityID(header):
    venue = raw_input('Enter the venue name: ')
    #Replace any spaces with %20.
    city = venue.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/venues?venueName=" + venue + "&p=1&sort=relevance"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    for key in data['city']:
        return key['mbid']

#Get a setlist
def getArtistSetlist(artistID, header):
    url = "https://api.setlist.fm/rest/1.0/artist/" + artistID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            #Get the first setlist that contains more than 0 songs
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response

def getVenueSetlist(cityID, header):
    url = "https://api.setlist.fm/rest/1.0/search/venue/" + cityID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            #Get the first setlist that contains more than 0 songs
            #This is to avoid events that don't have a populated setlist
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response

print spotify
print 'Please enter how you wish to search for looking up the setlist'
print
selection = raw_input('Enter 1 for artist name, 2 for date, 3 for venue: ')
print

#Input search term type (artist, date, or city/venue)
if selection == '1':
    name = raw_input("Enter artist name: ")
    artistID = getArtistID(headers, name)
    spotArtist = PlaylistMaker.searchTermsArtist(name)
    print artistID
    print getArtistSetlist(artistID, headers) #print data from setlist.fm
    print spotArtist
elif selection == '2':
    print('Enter the date.')
    month = raw_input('Enter the month: ')
    day = raw_input('Enter the day: ')
    year  = raw_input('Enter the year: ')
elif selection == '3':
    cityID = getCityID(headers)
    print cityID
    print getVenueSetlist(cityID, headers)
else:
    print('Not a valid input. Try again.')
