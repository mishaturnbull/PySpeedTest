# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:07:11 2018

@author: Misha
"""

import socket

from settings import REC_FILE, UPLOAD_URL, UPLOAD_PORT

HOST, PORT = ("mcv156.163.und.nodak.edu", 11356)  # hope this works

def upload():
    with open(REC_FILE, 'r') as f:
        lines = f.readlines()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((UPLOAD_URL, UPLOAD_PORT))
        for line in lines:
            sock.sendall(bytes(line, 'ascii'))
    with open(REC_FILE, 'w') as f:
        f.write('')
        # this is a *REALLY* good idea...
        # it prevents duplicate data being uploaded to the server
        # please, if you remove it, tell me why