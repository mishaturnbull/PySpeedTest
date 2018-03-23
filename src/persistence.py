# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:58:45 2018 by Misha

Handles where to put files when dealing with macOS app structures.
"""

import sys
import os
import platform

_IS_MAC = platform.system() == 'Darwin'

PATH_TO_APPEND_TO = ""

if _IS_MAC:
    # uuggghhhhhhhhhh

    # package directory structure is:
    #
    # PySpeedTest_v1.6.0_mac.app
    #  +- Contents
    #  |+- Framework
    #  |+- MacOS
    #  ||+- PySpeedTest_v1.6.0_mac
    #  ||+- (config.ini)
    #  |+- Resources
    #  ||+- icon_windowded.icns
    #  |+- Info.plist

    if getattr(sys, 'frozen', False):
        # bundled

        base_exec = sys.argv[0]

        if '.app' in base_exec:
            # graphical

            # path is like
            # /home/foo/bar/PST.app/Contents/MacOS/PySpeedTest_v1.6.0_mac
            # and should be like
            # /home/foo/bar

            temp_path = base_exec
            while not os.path.splitext(temp_path)[1] == '.app':
                print(temp_path)
                temp_path = os.path.split(temp_path)[0]
            # now we're level with the app bundle, go up one more and done!
            PATH_TO_APPEND_TO = os.path.split(temp_path)[0]

        else:
            # non-graphical
            PATH_TO_APPEND_TO = os.path.split(base_exec)[0]
    else:
        # live
        # nothing special needed
        pass


# stolen this bit of code from a reply to PyInstaller issue #1804
# https://github.com/pyinstaller/pyinstaller/
# issues/1804#issuecomment-332778156
# thanks, @StefGre!
def resource_path(relative_path):  # needed for bundling
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
