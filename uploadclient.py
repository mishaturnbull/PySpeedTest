# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:07:11 2018

@author: Misha
"""

import socket
import copy
try:
    import tkinter.messagebox as messagebox
except ImportError:
    import tkMessageBox as messagebox

from settings import REC_FILE, UPLOAD_URL, UPLOAD_PORT

def upload():
    with open(REC_FILE, 'r') as f:
        lines = f.readlines()
    outlines = copy.copy(lines)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((UPLOAD_URL, UPLOAD_PORT))
            for line in lines:
                sock.sendall(bytes(line, 'ascii'))
                outlines.remove(line)
    except Exception as exc:  # too general, I know... working on it.
        messagebox.showerror("Upload", "Couldn't upload data!\nTraceback:" +
                             exc.args)
    with open(REC_FILE, 'w') as f:
        f.writelines(outlines)
        # this is a *REALLY* good idea...
        # it prevents duplicate data being uploaded to the server
        # please, if you remove it, tell me why