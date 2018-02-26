# -*- coding: utf-8 -*-
"""
The oh-shit! file.

Downloads necessary dependencies if not found.
"""

import sys

if sys.version_info[0] == 2:
    from urllib import urlretrieve
elif sys.version_info[0] == 3:
    from urllib.request import urlretrieve

import zipfile # default on py2 and py3
import shutil  # ''
import os      # if you've installed python without os module, damn...

URLLIB3_URL = "https://github.com/shazow/urllib3/archive/master.zip"
PYSPEEDTEST_URL = "https://raw.githubusercontent.com/fopina/pyspeedtest/master/pyspeedtest.py"

class DependencyError(Exception): pass

def download_dependencies():
    print("Running emergency dependency download routine")
    CHANGES = False

    HAS_PYSPEEDTEST = True
    try:
        import pyspeedtest
    except ImportError:
        HAS_PYSPEEDTEST = False
    print("+++ pyspeedtest present: {}".format(str(HAS_PYSPEEDTEST)))
    
    HAS_URLLIB3 = True
    try:
        import urllib3
    except ImportError:
        HAS_URLLIB3 = False
    print("+++ urllib3 present: {}".format(str(HAS_URLLIB3)))
            
    if not HAS_URLLIB3:
        print("+++ attempting to download urllib3...")
        urlretrieve(URLLIB3_URL, 'urllib3.zip')
        print("+++ download complete, extracting")
        zipball = zipfile.ZipFile('urllib3.zip', 'r')
        zipball.extractall('.')
        zipball.close()
        shutil.copytree('./urllib3-master/urllib3', './urllib3')
        shutil.rmtree('./urllib3-master/')
        os.remove('urllib3.zip')
        CHANGES = True

        # test the install
        try:
            import urllib3
            print("+++ urllib3 installed successfully")
        except ImportError:
            print("+++ E: unable to install urllib3   <========")

    if not HAS_PYSPEEDTEST:
        print("+++ attempting to download pyspeedtest...")
        urlretrieve(PYSPEEDTEST_URL, 'pyspeedtest.py')
        print("+++ download complete")
        CHANGES = True
        
        # test the install to see if it worked
        try:
            import pyspeedtest
            print("+++ pyspeedtest installed successfully")
        except ImportError:
            print("+++ E: unable to install pyspeedtest   <========")
            
    if CHANGES:
        # quitting and making the user run again is wayyy easier than dealing
        # with UMR
        raise Exception("\n\n\nI think I fixed the problem -- restart and try again.\n\n\n")
