'''
general utilites for diff_tunes
'''
__author__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__license__ = "GNU GPLv3"
__maintainer__ = "Arjun Ray"
__status__ = "Development"
__version__ = "0.0.1"


def print_w_bar(p_string, bar_chr='='):
    '''wm
    prints p_string with same length bar_chr underline
    '''
    bar_string = bar_chr[0] * len(p_string)
    print '{0}\n{1}'.format(p_string, bar_string)
