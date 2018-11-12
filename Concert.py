import pprint
import sys

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import json

username = raw_input('Enter your Spotify username: ')
name = raw_input('Artist: ')
city = raw_input('City: ')
#venue = raw_input('Venue: ')
#int day, month, year
#date = raw_input('Month: ' + month + 'Day: ' + day +  'Year: ' + year)

spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + name, type='artist')
print results

#setlist.fm API
setCONSUMER_KEY = 'ecc895c8-fb79-4eab-be35-7d04744a15aa'

#spotify API
spotCONSUMER_KEY = '3817588cd345435c86c9a60e6c0cb70a'
spotCONSUMER_SECRET = 'ce6c55f9f3c343bb919d917257661a3b'
auth = spotipy.Spotify(spotCONSUMER_KEY, spotCONSUMER_SECRET)

client_credentials_manager = SpotifyClientCredentials(auth)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if len(sys.argv) > 3:
    username = sys.argv[1]
    playlist_id = sys.argv[2]
    track_ids = sys.argv[3:]
else:
    print "Usage: %s username playlist_id track_id ..." % (sys.argv[0],)
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope)

if token:
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    print results
else:
    print "Can't get token for", username
