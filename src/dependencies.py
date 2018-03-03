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

def download_dependencies(pst_loc=None, urllib3_loc=None,
                          quiet=False):
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
    
    HAS_TKINTER = True
    try:
        # darn you, python 2
        try:
            import Tkinter
        except ImportError:
            import tkinter
    except ImportError:
        HAS_TKINTER = False
    print("+++ tkinter present: {}".format(str(HAS_TKINTER)))
            
    if not HAS_URLLIB3:
        print("+++ attempting to download urllib3...")
        urlretrieve(URLLIB3_URL, 'urllib3.zip')
        print("+++ download complete, extracting")
        zipball = zipfile.ZipFile('urllib3.zip', 'r')
        zipball.extractall('.')
        zipball.close()
        shutil.copytree('./urllib3-master/urllib3', urllib3_loc or './urllib3')
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
        urlretrieve(PYSPEEDTEST_URL, pst_loc or 'pyspeedtest.py')
        print("+++ download complete")
        CHANGES = True
        
        # test the install to see if it worked
        try:
            import pyspeedtest
            print("+++ pyspeedtest installed successfully")
        except ImportError:
            print("+++ E: unable to install pyspeedtest   <========")
    
    if not HAS_TKINTER:
        msg = "\n\nI found a problem!  You don't have the tcl/tk module\n"
        msg += "installed, which is necessary for running GUI's.  Usually,\n"
        msg += "this happens on new-ish installations of Linux that are\n"
        msg += "missing the _tkinter package.  Usually, running the command\n"
        msg += "\n\nsudo apt-get install python-tkinter\n\nwill fix this.\n"
        raise Exception(msg)
            
    if CHANGES and not quiet:
        # quitting and making the user run again is wayyy easier than dealing
        # with UMR
        raise Exception("\n\n\nI think I fixed the problem -- restart and try again.\n\n\n")

if __name__ == '__main__':
    download_dependencies('src/pyspeedtest.py', 'src/urllib3/')
