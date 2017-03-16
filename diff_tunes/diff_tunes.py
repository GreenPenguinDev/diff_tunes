'''
__author__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__license__ = "GNU GPLv3"
__maintainer__ = "Arjun Ray"
__status__ = "Development"
__version__ = "0.0.1"
'''

import argparse
import os

import mutagen

# file extensions currently supported by Google Play Music
SUPPORTED_EXTENSIONS = ['mp3', 'm4a', 'wma', 'flac', 'ogg', 'mp4']

def print_w_bar(p_string, bar_chr='='):
    '''
    prints p_string with same length bar_chr underline
    '''
    bar_string = bar_chr[0] * len(p_string)
    print '{0}\n{1}'.format(p_string, bar_string)

def find_music_files(d_path, d_idx):
    '''
    populates music_files with music file info of the format, return list of
    such dicts, one dict per file
        {'filename':       f_name,
        'file_extention': ext,
        'dir_index':      d_idx,
        'abs_file_path':  abs_path}
    '''


    abs_d_path = os.path.abspath(d_path)
    print_w_bar('CURRENT DIR: "{}":'.format(abs_d_path), '-')

    # walk through files in each dir and get file info for files with SUPPORTED_EXTENSIONS

    return_list = []
    for d_path, d_names, f_names in os.walk(d_path):

        # filters files by extentions and accumulates file path info dicts

        filtered_f_names = [x for x in f_names if x.split('.')[-1] in SUPPORTED_EXTENSIONS]
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
    some shit
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

    def get_tags(abs_path, tag_map):
        '''
        returns meta tags dict based on tag_map from file at abs_path
        '''

        # get raw tag data

        raw_tag_data = mutagen.File(abs_path)

        # populate dictionary with tag values

        tag_dict = {}
        for key, val in tag_map.iteritems():
            tag_dict[key] = raw_tag_data.get(val)
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
        tags = get_tags(abs_path, tag_map)
        f_info['tags'] = tags

    return music_files

def main():
    '''
    generates diff for music files in dirs provided as args compared to tracks
    currently uploaded to Google Music Play. Allows for deleting files that have
    already been uploaded.
    '''

    '''
    -----------------------------
    CHECK/PARSE COMMAND LINE ARGS
    -----------------------------
    '''

    # parse

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

    '''
    ---------------------------------------
    FILTER MUSIC FILES, GET BASIC PATH INFO
    ---------------------------------------
    '''

    # get music file info dicts from each dir in dirs

    print 'FINDING MUSIC FILES\n{}'.format('=' * 20)
    music_files = []
    d_idx = 0
    for d_path in dirs:
        return_list, d_idx = find_music_files(d_path, d_idx)

        # add file info dicts from this dir to music_files

        music_files.extend(return_list)
        print '{} FILES FOUND'.format(len(return_list))

    print

    '''
    -------------------------
    GET ALBUM/ARTIST TAG INFO
    -------------------------
    '''

    # add album, artist, and other tags to music_files dict

    print 'GETTING TAGS\n{}'.format('=' * 20)
    music_files = append_artist_album_tags(music_files)
    print






if __name__ == '__main__':
    main()

'''
to do:
    
    for artist/album, deal with multiple tags mapping to each (use d_idx if neccesary, in artist[0] or intersect)
    clean up temp list extend
    add 
'''