# -*- coding: utf-8 -*-
"""
The oh-shit! file.

Downloads necessary dependencies if not found.
"""

import urllib  # default on py2 and py3

REQUESTS_URL = ":("
PYSPEEDTEST_URL = "https://raw.githubusercontent.com/fopina/pyspeedtest/master/pyspeedtest.py"

class DependencyError(Exception): pass

def download_dependencies():
    HAS_REQUESTS = True
    try:
        import requests
    except ImportError:
        HAS_REQUESTS = False

    HAS_PYSPEEDTEST = True
    try:
        import pyspeedtest
    except ImportError:
        HAS_PYSPEEDTEST = False
        
    if not HAS_REQUESTS:
        raise DependencyError("Missing `requests` library!")
        
    if not HAS_PYSPEEDTEST:
        urllib.urlretrieve(PYSPEEDTEST_URL, 'pyspeedtest.py')
        
        # test the install to see if it worked
        try:
            import pyspeedtest
        except ImportError:
            raise DependencyError("Can't install required module pyspeedtest")
        