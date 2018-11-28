import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import os
import json

import SpotifyPlaylist

tracks = []

#creates a list of song titles to be used for Spotify to search through
def createSetlist(setlist):
    #searches through the setlist information for the list of songs in the 'set' data
    for key in setlist.get('sets').get('set'):
        #finds the song titles listed in the setlist
        for key in key.get('song'):
            #adds the song title to the track list so the name can be searched in Spotify
            tracks.append(key['adds']
    return tracks

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
        #TODO: createSetlist(key)
                return key
    else:
        return response

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

def getSetlistID(artistName, year, venue, header):
    url = "https://api.setlist.fm/rest/1.0/search/setlists?artistName=" + artistName + "venueName=" + venue + "&year=" + year + "&p=1&sort=relevance"
    response = requests.get(url, headers = header, verify =True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            return key['id']
    else:
        return response

def getSetlist(setlistID, header):
    url = "https://api.setlist.fm/rest/1.0/setlist/" + setlistID + "/setlists"
    response = requests.get(url, headers = header, verify =True)
    data = response.json()
    if(response.ok):
        for key in data['setlist']:
            if len(key.get('sets').get('set')) > 0:
                return key
    else:
        return response
