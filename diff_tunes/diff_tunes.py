"""Compares Google Play Music vs music files in local folder(s).

generates diff for music files in dirs provided as args compared to tracks
currently uploaded to Google Music Play. Allows for deleting files that have
already been uploaded.

"""

__author__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__license__ = "GNU GPLv3"
__maintainer__ = "Arjun Ray"
__status__ = "Development"
__version__ = "0.0.1"

import argparse
import os
import sys

from getpass import getpass
from gmusicapi import Mobileclient

sys.path.append('./modules')
from general_utils import print_w_bar
from google_music_api_utils import authenticate
from music_file_utils import find_music_files, append_artist_album_tags

# file extensions currently supported by Google Play Music
SUPPORTED_EXTENSIONS = ['mp3', 'm4a', 'wmapre', 'flac', 'ogg', 'mp4']

def main():
    """Generate diffs, allow option to delete already uploaded files.

    """

    # -----------------------------
    # CHECK/PARSE COMMAND LINE ARGS
    # -----------------------------

    # parse args

    parser = argparse.ArgumentParser()
    parser.add_argument('dirs', nargs='+', type=str, help='directories containing music files')
    args = parser.parse_args()
    dirs = args.dirs

    # check that directories exist

    print_w_bar('CHECKING THAT DIRECTORIES EXIST')
    are_paths = [os.path.exists(d) for d in dirs]
    for i, d_bool in enumerate(are_paths):

        # remove non-existant directories

        if not d_bool:
            print '"{0}" is not a directory! skipping "{0}"...'.format(dirs.pop(i))

    print 'DONE!\n'


    # ----------------------------------------
    # AUTHENTICATE AND LOGIN TO GOOGLE ACCOUNT
    # ----------------------------------------

    # authenticate

    print_w_bar('AUTHENTICATING GOOGLE MUSIC PLAY')
    authenticate()

    # login

    print_w_bar('LOGIN TO YOUR GOOGLE ACCOUNT')
    logged_in = False
    while not logged_in:
        uname = raw_input('Username: ')
        pwd = getpass('Password: ')
        mbl_api = Mobileclient()
        logged_in = mbl_api.login(uname, pwd, Mobileclient.FROM_MAC_ADDRESS)
        if not logged_in:
            print '\nINCORRECT USERNAME OR PASSWORD!\n'
        else:
            print 'LOGGED IN!\n'

    # ---------------------------------------
    # FILTER MUSIC FILES, GET BASIC PATH INFO
    # ---------------------------------------

    # get music file info dicts from each d_path in dirs

    print 'FINDING MUSIC FILES\n{}'.format('=' * 20)
    music_files = []
    d_idx = 0
    for d_path in dirs:

        # get return_list w file info and d_idx for d_path

        abs_d_path = os.path.abspath(d_path)
        print_w_bar('CURRENT DIR: "{}":'.format(abs_d_path), '-')
        return_list, d_idx = find_music_files(d_path, d_idx, SUPPORTED_EXTENSIONS)

        # add file info dicts from this dir to music_files

        music_files.extend(return_list)
        print '{} FILES FOUND'.format(len(return_list))

    print


    # -------------------------
    # GET ALBUM/ARTIST TAG INFO
    # -------------------------


    # add album, artist, and other tags to music_files dict

    print 'GETTING TAGS\n{}'.format('=' * 20)
    music_files = append_artist_album_tags(music_files)
    print 'DONE!\n'

    # --------
    # RUN DIFF
    # --------

    # get a full song info list from Google Play Music
    # THIS IS STILL REALLY UGLY, FIX!

    all_gmusic_songs = mbl_api.get_all_songs()
    print len(all_gmusic_songs)
    for file_info in music_files:
        tags = file_info['tags']
        artist = tags['artist'][0] if isinstance(tags['artist'], list) else tags['artist']
        album = tags['album'][0] if isinstance(tags['album'], list) else tags['album']
        song_name = tags['song_name'][0] if isinstance(tags['song_name'], list) \
            else tags['song_name']

        try:
            artist = artist.lower()
        except AttributeError:
            pass
        try:
            album = album.lower()
        except AttributeError:
            pass
        try:
            song_name = song_name.lower()
        except AttributeError:
            pass
        matches = [song for song in all_gmusic_songs
                   if artist in [song['albumArtist'].lower(), song['artist'].lower()]
                   and song['album'].lower() == album
                   and song['title'].lower() == song_name]
        if not 0 < len(matches) < 2:
            print '{} matches '.format(len(matches)), album, artist, song_name


if __name__ == '__main__':
    main()

"""
to do:
    make autheticate function pure and less messy output too
    for artist/album, deal with multiple tags mapping to each (use d_idx if neccesary, in artist[0] or intersect)
    cases:
        add track num and track length comparison
        no album, song title, or artist: get trackname and compare
            trackname only tracks should be flagged for editing
            get all tags possible for each type, match across all that are provided by file
        duplicates should be compared by track length and track num
            duplicates should be compared by length, suggesting longer tracks possibly correct 
        
"""