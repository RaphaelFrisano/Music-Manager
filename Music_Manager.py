import time
import os
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook
import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials


def get_playlist_tracks(sp, username, playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

#Set up Spotify Connection 
client_id = 'd5ec1915e2b3452f87cd1f224551a935'
client_secret = '3e49c81210a34b4ea9ebdf90154b5df8'
username = '16r49f73ryoeuabwxqwgpimzs'
scope = 'user-library-read playlist-modify-public playlist-read-private'
redirect_uri='http://localhost:8888/callback'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)


# Initialisation
favouritesTracks = get_playlist_tracks(sp, username, "1W62xrI7rdqkrkT0xgbwTM")
DanceVibesPlaylist = "47wDz8QxSAsDOLB8c8HdCd"
HopPopVibesPlaylist = "tT9IzMkySrGHwNmhBBnB5w"
ClassicVibesPlaylist = "31159C1hoG2ZqZxtTLvBk2"
EasyVibesPlaylist = "7Gq1sXY7RZ3LSKm86bPn7v"
RockyVibesPlaylist = "67sSpThGjgTPiRnZ1S8GIW"
VibeCheckPlaylist = "4GtrzqGPZdCKA29WQWlRdJ"
DanceVibes = None
HopPopVibes = None
ClassicVibes = None
EasyVibes = None
RockyVibes = None
VibeCheck = None
Songnum = 0
SongnumEnd = 999


# Manage Music into Playlists
while Songnum < SongnumEnd:
    Songnum = Songnum + 1
    ParentGenres = "Cell from Excel"
    genres = ParentGenres.split(",")
    for genre in genres:
        if genre -like "Dance/Electronic":
            DanceVibes += favouritesTracks[Songnum]
        elif genre -like "Pop" or genre -like "HipHop"
            HopPopVibes += favouritesTracks[Songnum]
        elif genre -like "Classical":
            ClassicVibes += favouritesTracks[Songnum]
        elif genre -like "Easy Listening":
            EasyVibes += favouritesTracks[Songnum]
        elif genre -like "Rock" or genre -like "Metal": 
            RockyVibes += favouritesTracks[Songnum]
        else
            VibeCheck += favouritesTracks[Songnum]

#Connect to playlist
trackslist = sp.current_user_saved_tracks(limit=50, offset=0)

##Open Excel
#xlxwb = load_workbook(os.getcwd() + "/SongsList.xlsx")
#xlx = xlxwb['Tabelle1']
#
## Get songs
#excelStartFile = open(os.getcwd() + '/startline.txt', 'r+')
#row = excelStartFile.read()
#row = [int(s) for s in row.split() if s.isdigit()] # Get only numbers out of File
#row = row[0] # Get first number

trackslist = sp.current_user_saved_tracks(limit=50, offset=0)
offsetvar = 0
while(offsetvar <= trackslist['total']):
    
    trackslist = sp.current_user_saved_tracks(limit=50, offset=offsetvar)
    for songdict in trackslist['items']:
        # Get song Info
        songtitle = songdict['track']['name']
        artist = songdict['track']['artists'][0]['name']

        print("=======================|>")
        print("Title - " + songtitle)
        print("Artist - " + artist)

    
    offsetvar = offsetvar + 50

    # Add song to Excel
    xlx.cell(row = row, column = 1).value = str(artist)
    xlx.cell(row = row, column = 2).value = str(songtitle)
    xlx.cell(row = row, column = 3).value = str(time.asctime())

    row = row + 1