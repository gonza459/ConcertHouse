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
token = util.prompt_for_user_token(
    username = raw_input("Enter your username: "),
    scope = 'playlist-modify-private playlist-modify-public',
    #Enter Spotify API ID
    client_id ='3817588cd345435c86c9a60e6c0cb70a',
    #Enter Spotify API Secret
    client_secret ='ce6c55f9f3c343bb919d917257661a3b',
    #Enter Spotify API Redirect URI
    redirect_uri='http://spotify.com/us'
)
#create session token for spotify
spotify = SpotifyPlaylist.createSpotifyToken(token)
username = spotify.me()['id']

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'

headers = {'Accept': 'application/json', 'x-api-key': setCONSUMER_KEY}

print
#instructions for retrieving setlists
print 'You can now search for a setlist!'
print 'If you would like to create a playlist based on the most recent performance by an artist, enter 1.'
print 'If you would like the most recent concert performed at a venue, enter 2.'
print 'If you would like to create a playlist according to a specific performance, enter 3 to enter the artist name, venue name, and year.'
print

print 'Please enter how you wish to search for looking up the setlist'
selection = ''
while selection != '1' or '2' or '3':
    selection = raw_input('Enter 1 for artist name or 2 for venue or 3 for specific setlist: ')
    print

    #Input search term type (artist, or city/venue)
    if selection == '1':
        name = raw_input("Enter artist name: ")
        #Searches setlist.fm data for artist mbid
        artistID = SearchSetlist.getArtistID(headers, name)

        print 'Setlist: '
        print artistID # debug
        print SearchSetlist.getArtistSetlist(artistID, headers) #debug
        print

        #searches spotify data for info relating to artist name
        spotArtist = SpotifyPlaylist.searchTermsArtist(spotify, name)
        print 'Spotify: '
        print spotArtist #debug

        playlistName = raw_input("Enter the name of your Playlist: ")

        #Creates the playlist in the user's account
        playlist = SpotifyPlaylist.createSpotifyPlaylist(spotify, username, playlistName)

        #This retrieves the playlistID as jsut created by the user
        playlistID = SpotifyPlaylist.getSpotifyPlaylistID(spotify, username, playlistName)
        print playlistID #debug
        break

    #Search for most recent setlist according to venue name
    elif selection == '2':
        venue = raw_input('Enter the venue name: ')
        #searches setlit.fm data for venue id
        cityID = SearchSetlist.getVenueID(headers, venue)
        #print venue ID
        print cityID #debug
        print SearchSetlist.getVenueSetlist(cityID, headers) # debug

        playlistName = raw_input("Enter the name of your Playlist: ")

        #Creates the playlist in the user's account
        playlist = SpotifyPlaylist.createSpotifyPlaylist(spotify, username, playlistName)

        #This retrieves the playlistID as jsut created by the user
        playlistID = SpotifyPlaylist.getSpotifyPlaylistID(spotify, username, playlistName)
        print playlistID #debug
        break

    #Search for most recent setlist according to artist name, venue name, and year
    elif selection == '3':
        name = raw_input("Enter artist name: ")
        venue = raw_input('Enter the venue name: ')
        year = raw_input("Enter a year: ")

        #searches setlit.fm data for setlist id
        setlistID = SearchSetlist.getSetlistID(name, year, venue, headers)
        #takes setlistID and obtains the setlist data stored here
        FullSetlist = SearchSetlist.getSetlist(setlistID, headers)

        break

    else:
        print('Not a valid input. Try again.')
