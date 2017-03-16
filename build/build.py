'''
build module with all requirements and other files
'''

# make requiremnts.txt for pip

import subprocess
import os
REQ_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
subprocess.call(['pipreqs', '--force', REQ_PATH])
