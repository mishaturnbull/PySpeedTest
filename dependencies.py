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

REQUESTS_URL = "https://github.com/requests/requests/archive/master.zip"
PYSPEEDTEST_URL = "https://raw.githubusercontent.com/fopina/pyspeedtest/master/pyspeedtest.py"

class DependencyError(Exception): pass

def download_dependencies():
    print("Running emergency dependency download routine")
    HAS_REQUESTS = True
    try:
        import requests
    except ImportError:
        HAS_REQUESTS = False
    print("+++ requests present: {}".format(str(HAS_REQUESTS)))

    HAS_PYSPEEDTEST = True
    try:
        import pyspeedtest
    except ImportError:
        HAS_PYSPEEDTEST = False
    print("+++ pyspeedtest present: {}".format(str(HAS_PYSPEEDTEST)))

    if False: # or not HAS_REQUESTS:
        print("+++ attempting to download requests...")
        urlretrieve(REQUESTS_URL, 'requests.zip')
        print("+++ download complete, extracting")
        zipball = zipfile.ZipFile('requests.zip', 'r')
        zipball.extractall('.')
        zipball.close()
        shutil.copytree('./requests-master/requests', './requests')

        # test the install
        try:
            import requests
            print("+++ requests installed successfully")
        except ImportError:
            raise DependencyError("Missing `requests` library!")

    if not HAS_PYSPEEDTEST:
        print("+++ attempting to download pyspeedtest...")
        urlretrieve(PYSPEEDTEST_URL, 'pyspeedtest.py')
        print("+++ download complete")
        
        # test the install to see if it worked
        try:
            import pyspeedtest
            print("+++ pyspeedtest installed successfully")
        except ImportError:
            raise DependencyError("Can't install required module pyspeedtest")
