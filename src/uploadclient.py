# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:07:11 2018

@author: Misha
"""

import socket
import sys

try:
    import tkinter.messagebox as messagebox
except ImportError:
    import tkMessageBox as messagebox

# solution for issue #16
if sys.version_info[0] == 2:
    def encoder(string):
        return string.encode('ascii')
else:
    def encoder(string):
        return bytes(string, 'ascii')

from settings import REC_FILE, UPLOAD_URL, UPLOAD_PORT

def upload():
    with open(REC_FILE, 'r') as f:
        lines = f.readlines()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30)  # it's slow...
        s.connect((UPLOAD_URL, int(UPLOAD_PORT)))
        s.sendall(encoder(''.join(lines)))

    except Exception as exc:  # too general, I know... working on it.
        messagebox.showerror("Upload", "Couldn't upload data!\nTraceback: " +
                             repr(exc.args))
    with open(REC_FILE, 'w') as f:
        f.write('')
        # this is a *REALLY* good idea...
        # it prevents duplicate data being uploaded to the server
        # please, if you remove it, tell me why