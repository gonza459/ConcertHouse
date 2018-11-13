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
    #TODO : Add correct encoding so it can also manage non ANSI signs
    artist = artistToFind.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/artists?artistName=" + artist + "&p=1&sort=relevance"
    myResponse = requests.get(url, headers=header, verify=True)
    jData = json.loads(myResponse.content)
    for key in jData['artist']:
        return key['mbid']

#Get a setlist
def getSetlist(artistID, header):
    url = "https://api.setlist.fm/rest/1.0/artist/" + artistID + "/setlists"
    myResponse = requests.get(url, headers=header, verify=True)
    jDataSetSetList = json.loads(myResponse.content)
    #TODO : Add method to select more than latest setlist
    if(myResponse.ok):
        for key in jDataSetSetList['setlist']:
            #Get the first setlist that contains more than 0 songs
            #This is to avoid events that don't have a populated setlist
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        #TODO: Add some real error handling
        return myResponse

print 'Please enter how you wish to search for looking up the setlist'
print
selection = raw_input('Enter 1 for artist name, 2 for date, 3 for venue: ')
print
if selection == '1':
    getArtistID(headers)
elif selection == '2':
    print('Enter the date.')
    month = raw_input('Enter the month: ')
    day = raw_input('Enter the day: ')
    year  = raw_input('Enter the year: ')
elif selection == '3':
    venue = raw_input('Enter the venue name: ')
else:
    print('Not a valid input. Try again.')
