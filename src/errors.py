# -*- coding: utf-8 -*-
"""
Helpers for graphical error messages.

Should not require any 3rd-party or unsafe modules.

Py6 compliant.
"""

try:
    import tkinter as tk
    import tkinter.messagebox as messagebox
except ImportError:
    import Tkinter as tk
    import tkMessageBox as messagebox

# py2 proofing
import sys

def display_error(exception, raise_when_done=True):

    message = "wut"
    if sys.version_info[0] == 2:
        message = exception.message
    else:
        # assume python 3, doubt many are running py1...
        message = exception.args[0]

    messagebox.showerror('Error', message)

    if raise_when_done:
        # re-raise the exception when done...
        # makes it easier to trace errors for console users
        raise exception

def display_warning(message):

    messagebox.showwarning('Warning', message)
