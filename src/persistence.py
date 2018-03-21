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

        ext = os.path.splitext(base_exec)[1]
        if ext == 'app':
            # graphical

            # path is like
            # /home/foo/bar/baz/PST.app
            # and should be like
            # /home/foo/bar/baz
            PATH_TO_APPEND_TO = os.path.split(base_exec)[0]

        elif ext == '':
            # non-graphical
            PATH_TO_APPEND_TO = os.path.split(base_exec)[0]
        else:
            assert False, base_exec
    else:
        # live
        # nothing special needed
        pass

print(base_exec, PATH_TO_APPEND_TO)
