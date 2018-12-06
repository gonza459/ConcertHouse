import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import os
import json

import SpotifyPlaylist


#Get the MusicBrainz ID for the artist
def getArtistID(header, name):
    #Replace any spaces with %20.
    artist = name.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/artists?artistName=" + artist + "&p=1&sort=relevance"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    for key in data['artist']:
        return key['mbid']

#Get a setlist
def getArtistSetlist(artistID, header):
    url = "https://api.setlist.fm/rest/1.0/artist/" + artistID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            #Get the first setlist that contains more than 0 songs so to not
            #get back a list of a not performed concert yet
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response

def createSetlist(Setlist):
    tracks = []
    for key in Setlist.get('sets').get('set'):
        for key in key.get('song'):
            tracks.append(key['name'])
        return tracks

#Get the ID for the venue
def getVenueID(header, name):
    #Replace any spaces with %20.
    city = name.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/venues?name=" + city + "&p=1&sort=relevance"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    for key in data['venue']:
        return key['id']

def getVenueSetlist(cityID, header):
    url = "https://api.setlist.fm/rest/1.0/venue/" + cityID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            #Get the first setlist that contains more than 0 songs so to not get back a list of a not performed concert yet
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response

def getVenueArtistName(cityID, header):
    url = "https://api.setlist.fm/rest/1.0/venue/" + cityID + "/setlists"
    response = requests.get(url, headers=header, verify=True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            if len(key.get('sets').get('set')) > 0:
                return key['artist']['name']
    else:
        return response


def getSetlistID(artistName, year, venue, header):
    artist = artistName.replace(" ", "%20")
    city = venue.replace(" ", "%20")
    url = "https://api.setlist.fm/rest/1.0/search/setlists?artistName=" + artist + "&year=" + year + "&p=1&venueName=" + city + "&p=1&sort=relevance"
    response = requests.get(url, headers = header, verify =True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            return key['id']
    else:
        return response

def getSetlist(setlistID, header):
    url = "https://api.setlist.fm/rest/1.0/setlist/" + setlistID
    response = requests.get(url, headers = header, verify =True)
    data = response.json()
    if(response.ok):
        return data
    else:
        return response
