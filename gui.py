# -*- coding: utf-8 -*-
"""
Graphical user interface for speed test.

Hopefully useful.
"""

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
    
import webbrowser
import subprocess

from main import main as loop_test

class SpeedTesterGUI(object):
    
    def __init__(self):
        self.root = tk.Tk()
        self.guivars = {'status': 'stopped',
                        'lasttest': {'ping': 0, 'up': 0, 'down': 0},
                        'avg': {'ping': 0, 'up': 0, 'down': 0},
                        }
        self.location = "-- ENTER LOCATION --"
        
        
        self.init_gui()
        self.root.mainloop()
        
    def start(self):
        self.guivars['status'] = 'running'
        self.status_label.config(text="Status: running")
    
    def stop(self):
        self.guivars['status'] = 'stopped'
        self.status_label.config(text="Status: stopped")
    
    def make_analysis_file(self):
        pass
    
    def upload_data(self):
        pass
    
    def edit_config(self):
        pass
    
    def resnet(self):
        webbrowser.open("http://und.edu/web-support/request.cfm")
        
    # here we go... avoid this code.  it's bad.
    def init_gui(self):
        self.root.title("Internet Speed Tester")
        
        self.status_label = tk.Label(self.root, text="Status: " +
                                                self.guivars['status'],
                                     )
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        self.start_button = tk.Button(self.root, text="Start",
                                      command=self.start)
        self.start_button.grid(row=1, column=1, sticky=tk.E)
        self.stop_button = tk.Button(self.root, text="Stop",
                                     command=self.stop)
        self.stop_button.grid(row=1, column=2, sticky=tk.W)
        
        self.location_label = tk.Label(self.root, text="Location:")
        self.location_label.grid(row=2, column=0, sticky=tk.W)
        self.location_entry = tk.Entry(self.root, width=17)
        self.location_entry.grid(row=2, column=1, columnspan=2,
                                 sticky=tk.W)
        
        self.makefile_button = tk.Button(self.root, text="Create analysis file",
                                         command=self.make_analysis_file)
        self.makefile_button.grid(row=3, column=0, columnspan=2,
                                  sticky=tk.W)
        self.upload_button = tk.Button(self.root, text="Upload",
                                      command=self.upload_data)
        self.upload_button.grid(row=3, column=1, sticky=tk.W)
        
        self.last_test_label = tk.Label(self.root, text="Last: ")
        self.last_test_label.grid(row=4, column=0, sticky=tk.W)
        
        self.avg_test_label = tk.Label(self.root, text="Avg.: ")
        self.avg_test_label.grid(row=5, column=0, sticky=tk.W)
        
        self.config_button = tk.Button(self.root, text="Edit configuration",
                                       command=self.edit_config)
        self.config_button.grid(row=7, column=0, sticky=tk.W)
        
        self.resnet_button = tk.Button(self.root, text="ResNet",
                                       command=self.resnet)
        self.resnet_button.grid(row=7, column=1, sticky=tk.W)