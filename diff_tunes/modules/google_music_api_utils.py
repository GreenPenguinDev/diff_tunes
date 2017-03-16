'''
utils for interacting with the google music api using gmusicapi
'''
__author__ = "Arjun Ray"
__email__ = "deconstructionalism@gmail.com"
__license__ = "GNU GPLv3"
__maintainer__ = "Arjun Ray"
__status__ = "Development"
__version__ = "0.0.1"

import sys

from gmusicapi import Musicmanager

def authenticate():
    '''
    authenticate OAUTH credentials, if non-existent, set them up
    '''
    mm_api = Musicmanager()
    num_tries = 0
    while num_tries < 5:

        logged_in = mm_api.login()
        if not logged_in:
            try:
                print 'NO OAUTH CREDENTIALS FOUND'
                print 'copy full link below and make sure to select an ' \
                      'account that has google play music'
                mm_api.perform_oauth()
            except:
                print 'INVALID AUTH CODE, UNABLE TO AUTHENTICATE! EXITING...'
                sys.exit(0)
        else:
            print 'AUTHENTICATION SUCCESSFUL!\n'
            break
        num_tries += 1



    # mm.perform_oauth()
    # print stdout_to_line_array(mm.login)
    # api = Mobileclient()


    # from cStringIO import StringIO
    # import sys

    # class Capturing(list):
    #     def __enter__(self):
    #         self._stdout = sys.stdout
    #         sys.stdout = self._stringio = StringIO()
    #         return self
    #     def __exit__(self, *args):
    #         self.extend(self._stringio.getvalue().splitlines())
    #         del self._stringio    # free up some memory
    #         sys.stdout = self._stdout

    # sys.stdout.write( chr(8))
    # sys.stdout.flush()

    # # with Capturing() as output:
    # proc = subprocess.Popen(["python", "-c", "from gmusicapi import Musicmanager; mm = Musicmanager(); print mm.login()"], stdout=subprocess.PIPE)
    # out = proc.communicate()[0]
    # print out.upper()
