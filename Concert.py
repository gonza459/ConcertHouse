import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import os
import json

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'
headers = {'Accept': 'application/json', 'x-api-key': setCONSUMER_KEY}

#Get the MusicBrainz ID for the artist
def getArtistID(header):
    name = raw_input("Enter artist name: ")
    #Replace any spaces with %20.
    artist = name.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/artists?artistName=" + artist + "&p=1&sort=relevance"
    response = requests.get(url, headers=header, verify=True)
    jData = json.loads(response.content)
    for key in jData['artist']:
        return key['mbid']

def getCityID(header):
    venue = raw_input('Enter the venue name: ')
    #Replace any spaces with %20.
    city = cityToFind.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/artists?artistName=" + artist + "&p=1&sort=relevance"
    response = requests.get(url, headers=header, verify=True)
    jData = json.loads(response.content)
    for key in jData['city']:
        return key['mbid']

#Get a setlist
def getArtistSetlist(artistID, header):
    url = "https://api.setlist.fm/rest/1.0/artist/" + artistID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    jSetlistData = json.loads(response.content)
    #TODO : Add method to select more than latest setlist
    if(response.ok):
        for key in jSetlistData['setlist']:
            #Get the first setlist that contains more than 0 songs
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response

def getVenueSetlist(cityID, header):
    url = "https://api.setlist.fm/rest/1.0/search/venue/" + cityID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    jSetlistData = json.loads(response.content)
    #TODO : Add method to select more than latest setlist
    if(response.ok):
        for key in jSetlistData['setlist']:
            #Get the first setlist that contains more than 0 songs
            #This is to avoid events that don't have a populated setlist
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response

print 'Please enter how you wish to search for looking up the setlist'
print
selection = raw_input('Enter 1 for artist name, 2 for date, 3 for venue: ')
print

#Input search term type (artist, date, or city/venue)
if selection == '1':
    artistID = getArtistID(headers)
    print artistID
    getArtistSetlist(artistID, headers)
elif selection == '2':
    print('Enter the date.')
    month = raw_input('Enter the month: ')
    day = raw_input('Enter the day: ')
    year  = raw_input('Enter the year: ')
elif selection == '3':
    venue = raw_input('Enter the venue name: ')
else:
    print('Not a valid input. Try again.')
