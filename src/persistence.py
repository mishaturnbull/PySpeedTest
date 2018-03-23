# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:58:45 2018 by Misha

Handles where to put files when dealing with macOS app structures.
"""

import sys
import os
import platform

_IS_MAC = platform.system() == 'Darwin'


# stolen this bit of code from a reply to PyInstaller issue #1804
# https://github.com/pyinstaller/pyinstaller/
# issues/1804#issuecomment-332778156
# thanks, @StefGre!
# modifications were made, however, to suit the cross-platform nature
# of this program
def resource_path(relative_path):  # needed for bundling
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if not _IS_MAC:
        return relative_path
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
