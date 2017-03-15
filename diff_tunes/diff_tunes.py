'''
__author__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__license__ = "GNU GPLv3"
__maintainer__ = "Arjun Ray"
__status__ = "Development"
__version__ = "0.0.1"
'''

import argparse
import mutagen
import os
import re

# file extensions currently supported by Google Play Music
SUPPORTED_EXTENSIONS = ['mp3', 'm4a', 'wma', 'flac', 'ogg', 'm4p', 'm4a']

def print_w_bar(p_string, bar_chr='='):
    '''
    prints p_string with same length bar_chr underline
    '''
    bar_string = bar_chr[0] * len(p_string)
    print '{0}\n{1}'.format(p_string, bar_string)

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
    print 'DONE!'
    print'\n\n'

    '''
    ---------------------------------------
    FILTER MUSIC FILES, GET BASIC PATH INFO
    ---------------------------------------
    '''

    # get music file names in directories

    def filter_by_filetype(f_name):
        '''
        filters file name (f_name) by extention in SUPPORTED_EXTENSIONS
        '''
        split_name = re.split(r'^[\w,\s-]*\.', f_name)
        ext = split_name[1] if len(split_name) == 2 else None
        return ext in SUPPORTED_EXTENSIONS

    print 'FINDING MUSIC FILES\n{}'.format('=' * 20)

    # populates music_files with music file info of the format
    # {'filename':       f_name,
    #  'file_extention': ext,
    #  'dir_index':      d_idx,
    #  'abs_file_path':  abs_path}

    music_files = []
    d_idx = 0
    for d in dirs:
        abs_d_path = os.path.abspath(d)
        print_w_bar('CURRENT DIR: "{}":'.format(abs_d_path), '-')

        # walk through files in each dir and get file info for files with SUPPORTED_EXTENSIONS

        temp_list = []
        for d_path, d_names, f_names in os.walk(d):

            # accumulates file info dicts

            filtered_f_names = filter(filter_by_filetype, f_names)
            for f_name in filtered_f_names:
                ext = re.split(r'^[\w,\s-]*\.', f_name)[1]
                rel_path = os.path.join(d_path, f_name)
                abs_path = os.path.abspath(rel_path)
                temp_dict = {'filename': f_name, 'file_extension': ext, 'dir_index': d_idx, 'abs_file_path': abs_path}
                temp_list.append(temp_dict)
            d_idx += 1

        # add file info dicts from this dir to music_files

        n_files = len(temp_list)
        print '{} FILES FOUND\n'.format(n_files)
        music_files.extend(temp_list)
    print

    '''
    -------------------------
    GET ALBUM/ARTIST TAG INFO
    -------------------------
    '''

    for f_info in music_files:
        (f_name, ext, d_idx, f_path) = f_info
        print d_idx
        print f_name
        print ext
        try:
            print mutagen.File(f_path)['TPE1']
        except:
            try:
                print mutagen.File(f_path)['\xa9ART']
            except:
                print mutagen.File(f_path)['artist']


if __name__ == '__main__':
    main()

'''
to do:
    keep string types or translate non-lossy to unicode for id tags
    figure out file type to tag procurement mapping for [artist, album]
    for artist/album, deal with multiple tags mapping to each (use d_idx if neccesary, in artist[0] or intersect)
    clean up temp list extend
    add 
'''