# -*- coding: utf-8 -*-
"""
The oh-shit! file.

Downloads necessary dependencies if not found.
"""

import sys
import zipfile  # default on py2 and py3
import shutil   # ''
import os       # if you've installed python without os module, damn...

# lazy man's argparse
SILENT = False
if '--silent' in sys.argv:
    SILENT = True

if sys.version_info[0] == 2:
    from urllib import urlretrieve
elif sys.version_info[0] == 3:
    from urllib.request import urlretrieve

URLLIB3_URL = "https://github.com/shazow/urllib3/archive/master.zip"
PYSPEEDTEST_URL = "https://raw.githubusercontent.com/fopina/pyspeedtest/master/pyspeedtest.py"


class DependencyError(Exception): pass


def download_dependencies(pst_loc=None, urllib3_loc=None,
                          quiet=False):
    print("Running emergency dependency download routine")
    changes_made = False

    has_pyspeedtest = True
    try:
        import pyspeedtest
    except ImportError:
        has_pyspeedtest = False
    print("+++ pyspeedtest present: {}".format(str(has_pyspeedtest)))

    has_urllib3 = True
    try:
        import urllib3
    except ImportError:
        has_urllib3 = False
    print("+++ urllib3 present: {}".format(str(has_urllib3)))

    has_tkinter = True
    try:
        # darn you, python 2
        try:
            import Tkinter
        except ImportError:
            import tkinter
    except ImportError:
        has_tkinter = False
    print("+++ tkinter present: {}".format(str(has_tkinter)))

    if not has_urllib3:
        print("+++ attempting pip install of urllib3...")
        result = os.system('pip install urllib3')
        if result == 0:
            # okay, we installed successfully, break here
            print("+++ pip install successful")
        else:
            print("+++ attempting to download urllib3...")
            urlretrieve(URLLIB3_URL, 'urllib3.zip')
            print("+++ download complete, extracting")
            zipball = zipfile.ZipFile('urllib3.zip', 'r')
            zipball.extractall('.')
            zipball.close()
            shutil.copytree('./urllib3-master/urllib3', urllib3_loc or './urllib3')
            shutil.rmtree('./urllib3-master/')
            os.remove('urllib3.zip')
        changes_made = True

        # test the install
        try:
            import urllib3
            print("+++ urllib3 installed successfully")
        except ImportError:
            print("+++ E: unable to install urllib3   <========")

    if not has_pyspeedtest:
        print("+++ attempting pip install of pyspeedtest...")
        result = os.system('pip install pyspeedtest')
        if result == 0:
            # success
            print("+++ pip install successful")
        else:
            print("+++ attempting to download pyspeedtest...")
            urlretrieve(PYSPEEDTEST_URL, pst_loc or 'pyspeedtest.py')
            print("+++ download complete")
            changes_made = True

        # test the install to see if it worked
        try:
            import pyspeedtest
            print("+++ pyspeedtest installed successfully")
        except ImportError:
            print("+++ E: unable to install pyspeedtest   <========")

    if not has_tkinter:
        msg = "\n\nI found a problem!  You don't have the tcl/tk module\n"
        msg += "installed, which is necessary for running GUI's.  Usually,\n"
        msg += "this happens on new-ish installations of Linux that are\n"
        msg += "missing the _tkinter package.  Usually, running the command\n"
        msg += "\n\nsudo apt-get install python-tkinter\n\nwill fix this.\n"
        raise Exception(msg)

    if changes_made and not quiet:
        # quitting and making the user run again is wayyy easier than dealing
        # with UMR
        raise Exception("\n\n\nI think I fixed the problem -- restart and try again.\n\n\n")


if __name__ == '__main__':
    download_dependencies('src/pyspeedtest.py', 'src/urllib3/', SILENT)
