# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:07:11 2018

@author: Misha
"""

import socket
import sys
import threading

import errors

from settings import REC_FILE, UPLOAD_URLS, UPLOAD_PORT

try:
    import tkinter as tk
    import tkinter.messagebox as messagebox
except ImportError:
    import Tkinter as tk
    import tkMessageBox as messagebox

# solution for issue #16
if sys.version_info[0] == 2:
    def encoder(string):
        return string.encode('ascii')
else:
    def encoder(string):
        return bytes(string, 'ascii')

class UploadProcess(threading.Thread):

    timeout = 30

    def __init__(self, handler):

        # init the thread
        threading.Thread.__init__(self)

        self.handler = handler
        self.lines = None
        self.socket = None
        self.has_connection = False

    def establish_connection(self):
        self.handler.set_label(1, 'Beginning connection searching on port ' +
                               str(UPLOAD_PORT))
        # ;-)
        secs = self.timeout * len(UPLOAD_URLS)
        self.handler.set_label(2, ('This could take up to {} seconds, ' +
                                   'please be patient').format(str(secs)))

        for url in UPLOAD_URLS:
            try:
                self.handler.set_label(1,
                                       "Attempting to connect to " + url +
                                       ":" + str(UPLOAD_PORT))
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(self.timeout)  # it's slow...
                self.socket.connect((url, int(UPLOAD_PORT)))
                self.has_connection = True
                self.handler.set_label(1, "Connected to " + url + ":" +
                                       str(UPLOAD_PORT))
                break

            # socket.error is the error returned on timeout
            # in Python 2 (e.g. MacOS)
            except (socket.gaierror, socket.timeout, socket.error):
                # Welp, that one didn't work... keep going!
                self.has_connection = False

        if not self.has_connection:
            self.handler.set_label(1, 'No connection established')

        return self.has_connection

    def send_data(self):
        if not self.has_connection:
            raise ValueError("Can't upload data with no connection!")

        self.handler.set_label(2, 'Reading file')

        try:
            with open(REC_FILE, 'r') as infile:
                self.lines = infile.readlines()
        except IOError:
            self.lines = []  # let the handler on the next step handle this

        if not self.lines:
            errors.display_error(IOError("File contains no data or is not"
                                         " found on disk!"))
            return

        for line in self.lines:
            self.handler.set_label(2, line)
            encoded = encoder(line)
            self.socket.sendall(encoded)

        self.handler.set_label(2, 'Clearing file')
        with open(REC_FILE, 'w') as handle:
            handle.write('')

    def run(self):
        self.establish_connection()
        self.send_data()

    def join(self, timeout=None):
        super(UploadProcess, self).join(timeout)

class Uploader(object):

    def __init__(self, handler=None):
        self.handler = handler

        self.subprocess = UploadProcess(self)

        self.window = self.label1 = self.label2 = None

    def upload(self):

        self.subprocess.start()

    def set_label(self, num, message):
        if self.handler is None:
            return

        label = self.label2 if (num - 1) else self.label1

        label.config(text=message)

    def build_window(self):
        if self.handler is None:
            return  # we can't do anything without a root.  likely running
                    # in terminal mode anyways, where the user doesn't want
                    # a GUI

        self.window = tk.Toplevel(self.handler.root)
        self.window.title("Data Upload Interface")

        self.label1 = tk.Label(self.window, text="Waiting for connection")
        self.label1.grid(row=0, column=0, sticky=tk.E+tk.W)

        self.label2 = tk.Label(self.window, text="Please be patient"*50)
        self.label2.grid(row=1, column=0, sticky=tk.E+tk.W)

        self.set_label(1, ' ')
        self.set_label(2, ' ')
