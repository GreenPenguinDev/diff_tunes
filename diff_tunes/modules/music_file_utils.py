'''
music file search and manipulations utlities for diff_tunes
'''
__author__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__license__ = "GNU GPLv3"
__maintainer__ = "Arjun Ray"
__status__ = "Development"
__version__ = "0.0.1"

import os

import mutagen

def find_music_files(d_path, d_idx, supported_extensions):
    '''
    given a directory path d_path, populates music_files list with music file info in
    the format:
        {'filename':       f_name,
        'file_extention': ext,
        'dir_index':      d_idx,
        'abs_file_path':  abs_path}
    with on such dict per found music file.
    also takes a d_idx (a directory index, monotonically increasing from 0 and initiated
    in greater scope). returns music_files, d_idx
    '''

    # walk through files in each dir and get file info for files with SUPPORTED_EXTENSIONS

    return_list = []
    for d_path, d_names, f_names in os.walk(d_path):

        # filters files by extentions and accumulates file path info dicts

        filtered_f_names = [x for x in f_names if x.split('.')[-1] in supported_extensions]
        for f_name in filtered_f_names:
            ext = f_name.split('.')[-1]
            rel_path = os.path.join(d_path, f_name)
            abs_path = os.path.abspath(rel_path)
            temp_dict = {
                'filename': f_name,
                'file_extension': ext,
                'dir_index': d_idx,
                'abs_file_path': abs_path
            }
            return_list.append(temp_dict)
        d_idx += 1

    return return_list, d_idx

def append_artist_album_tags(music_files):
    '''
    take a list of file info dicts music_files returned by find_music_files() and
    gets meta tag information as a dict for each file, then append this dict to each file
    info dict as 'tag' key and returns the modified music_files dict.
    '''

    # maps of format key='tag display name', val='prop name of tag in raw info'

    mp3_tag_map = {
        'composer': 'TCOM',
        'song_name': 'TIT2',
        'artist': 'TPE1',
        'album': 'TALB',
        'orig_album': 'TOAL'
    }

    mp4_tag_map = {
        'composer': '\xa9wrt',
        'song_name': '\xa9nam',
        'artist': '\xa9ART',
        'album_artist': 'aART',
        'album': '\xa9alb',
    }

    vorbis_tag_map = {
        'song_name': 'title',
        'artist': 'artist',
        'performer': 'performer',
        'album': 'album',
    }

    def get_tags(abs_path, tag_map, ext):
        '''
        returns meta tags dict based on tag_map from file at abs_path
        '''

        # get raw tag data

        raw_tag_data = mutagen.File(abs_path)

        # populate dictionary with tag values

        tag_dict = {}
        for key, val in tag_map.iteritems():
            tag_val = raw_tag_data.get(val)

            # pretty print and extract ID3 tags,

            if ext == 'mp3' and tag_val <> None:
                tag_dict[key] = tag_val.pprint().split('=')[1]

            # simply assign non-ID3 tags

            else:
                tag_dict[key] = tag_val
        return tag_dict


    for f_info in music_files:

        # unpack f_info values

        ext = f_info['file_extension']
        abs_path = f_info['abs_file_path']

        # select tag map based on ext type

        type_to_map = [
            [['mp3'], mp3_tag_map],
            [['m4a', 'mp4'], mp4_tag_map],
            [['flac', 'ogg'], vorbis_tag_map]
        ]

        tag_map = [x[1] for x in type_to_map if ext in x[0]][0]
        tags = get_tags(abs_path, tag_map, ext)
        f_info['tags'] = tags

    return music_files
