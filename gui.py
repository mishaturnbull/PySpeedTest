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
import threading
import time

from pyspeedtest import pretty_speed

from main import test_once
from settings import REC_FILE, LOCATION, FREQ, VERBOSITY, FORCE_SERVER, \
                     ANALYZE_FILE, ANALYTICS_REC_FILE, STANDARDS_ENABLE, \
                     STANDARD_PING, STANDARD_UP, STANDARD_DOWN, parser

class SpeedTesterThread(threading.Thread):

    def __init__(self, handler):
        threading.Thread.__init__(self)
        self.last_result = {'ping': 0, 'up': 0, 'down': 0}
        self.stoprequest = threading.Event()
        self.handler = handler

    def run(self):
        self.handler.thread_status.config(text="Thread status: alive")
        while not self.stoprequest.isSet():
            self.handler.thread_status.config(text="Thread status: testing")
            newline, time_diff, self.last_result = test_once(
                self.handler.location_entry.get())
            self.handler.thread_status.config(
                text="Thread status: writing results")
            with open(REC_FILE, 'a') as record:
                record.write(newline)
            self.handler.update_statistics()
            # check again for stop request here -- otherwise, we'll wait
            # to the next test unnecessarily
            if not self.stoprequest.isSet():
                self.handler.thread_status.config(text="Thread status: waiting")
                time.sleep(time_diff)
        self.handler.status_label.config(text="Status: stopped")
        self.handler.thread_status.config(text="Thread status: dead")

    def join(self, timeout=None):
        self.stoprequest.set()
        super(SpeedTesterThread, self).join(timeout)


class SpeedTesterGUI(object):

    def __init__(self):
        self.root = tk.Tk()
        self.location = "-- ENTER LOCATION --"

        self.lasttest = {'ping': 0, 'up': 0, 'down': 0}
        self.avg = {'ping': 0, 'up': 0, 'down': 0}
        self.ntests = 0

        self.thread = SpeedTesterThread(self)

        self.init_gui()
        self.root.mainloop()

    def update_statistics(self):
        self.lasttest = self.thread.last_result
        self.ntests += 1
        self.avg['ping'] = self.avg['ping'] + ((self.lasttest['ping'] -
                                                self.avg['ping']) /
                                               self.ntests)
        self.avg['down'] = self.avg['down'] + ((self.lasttest['down'] -
                                                self.avg['down']) /
                                               self.ntests)
        self.avg['up'] = self.avg['up'] + ((self.lasttest['up'] -
                                            self.avg['up']) /
                                           self.ntests)

        last_str = "Last: Ping: {ping}ms / {up}\u2191 / {down}\u2193".format(
            ping=self.lasttest['ping'],
            up=pretty_speed(self.lasttest['up']),
            down=pretty_speed(self.lasttest['down']))
        avg_str = "Avg: Ping: {ping}ms / {up}\u2191 / {down}\u2193".format(
            ping=self.avg['ping'],
            up=pretty_speed(self.avg['up']),
            down=pretty_speed(self.avg['down']))

        self.last_test_label.config(text=last_str)
        self.avg_test_label.config(text=avg_str)

    def start(self):
        self.lasttest = {'ping': 0, 'up': 0, 'down': 0}
        self.avg = {'ping': 0, 'up': 0, 'down': 0}
        self.ntests = 0
        self.status_label.config(text="Status: running")
        self.thread.start()

    def stop(self):
        self.status_label.config(text="Status: stopping")
        self.thread.join(0.5)

    def make_analysis_file(self):
        import analytics   # this should do the trick...

    def upload_data(self):
        pass

    def edit_config(self):
        cfgmen = tk.Toplevel(self.root)
        cfgmen.wm_title("Configuration")

        def set_vars():
            parser['Speedtester']['rec_file'] = entry_recfile.get()
            parser['Speedtester']['location'] = entry_location.get()
            parser['Speedtester']['freq'] = entry_freq.get()
            parser['Speedtester']['verbosity'] = entry_verbosity.get()
            parser['Speedtester']['force_server'] = entry_server.get()
            parser['Analytics']['analyze_file'] = entry_afile.get()
            parser['Analytics']['analytics_rec_file'] = entry_arecfile.get()
            parser['Analytics']['standards_enable'] = str(bool(standvar.get()))
            parser['Analytics']['standard_ping'] = entry_stan_ping.get()
            parser['Analytics']['standard_up'] = entry_stan_up.get()
            parser['Analytics']['standard_down'] = entry_stan_down.get()

            with open("config.ini", 'w') as configfile:
                parser.write(configfile)

        def refresh():
            entry_recfile.delete(0, 'end')
            entry_recfile.insert(0, REC_FILE)

            entry_location.delete(0, 'end')
            entry_location.insert(0, LOCATION)

            entry_freq.delete(0, 'end')
            entry_freq.insert(0, FREQ)

            entry_verbosity.delete(0, 'end')
            entry_verbosity.insert(0, VERBOSITY)

            entry_server.delete(0, 'end')
            entry_server.insert(0, str(FORCE_SERVER))

            entry_afile.delete(0, 'end')
            entry_afile.insert(0, str(ANALYZE_FILE))

            entry_arecfile.delete(0, 'end')
            entry_arecfile.insert(0, ANALYTICS_REC_FILE)

            standvar.set(int(bool(STANDARDS_ENABLE)))
            _updopt()

            entry_stan_ping.delete(0, 'end')
            entry_stan_ping.insert(0, STANDARD_PING)

            entry_stan_up.delete(0, 'end')
            entry_stan_up.insert(0, STANDARD_UP)

            entry_stan_down.delete(0, 'end')
            entry_stan_down.insert(0, STANDARD_DOWN)


        setbutton = tk.Button(cfgmen, text="Apply", command=set_vars)
        setbutton.grid(row=0, column=0, sticky=tk.W)

        refreshbutton = tk.Button(cfgmen, text="Refresh", command=refresh)
        refreshbutton.grid(row=0, column=1, sticky=tk.E)

        label_sec_speedtest = tk.Label(cfgmen,
                                       text="===== SPEEDTESTER SETTINGS =====")
        label_sec_speedtest.grid(row=1, column=0, columnspan=2)

        label_recfile = tk.Label(cfgmen, text="Record file name:")
        label_recfile.grid(row=2, column=0, sticky=tk.W)
        entry_recfile = tk.Entry(cfgmen, width=40)
        entry_recfile.grid(row=2, column=1, sticky=tk.W)

        # TODO: resize location entry size to appropriate length
        label_location = tk.Label(cfgmen, text="Recording location:")
        label_location.grid(row=3, column=0, sticky=tk.W)
        entry_location = tk.Entry(cfgmen, width=40)
        entry_location.grid(row=3, column=1, sticky=tk.W)

        label_freq = tk.Label(cfgmen, text="Testing frequency (min):")
        label_freq.grid(row=4, column=0, sticky=tk.W)
        entry_freq = tk.Entry(cfgmen, width=10)
        entry_freq.grid(row=4, column=1, sticky=tk.W)

        label_verbosity = tk.Label(cfgmen, text="Verbosity: (0-3):")
        label_verbosity.grid(row=5, column=0, sticky=tk.W)
        entry_verbosity = tk.Entry(cfgmen, width=2)
        entry_verbosity.grid(row=5, column=1, sticky=tk.W)

        label_server = tk.Label(cfgmen, text="Force speedtest server:")
        label_server.grid(row=6, column=0, sticky=tk.W)
        entry_server = tk.Entry(cfgmen, width=40)
        entry_server.grid(row=6, column=1, sticky=tk.W)

        label_sec_analytics = tk.Label(cfgmen,
                                       text="===== ANALYTICS SETTINGS =====")
        label_sec_analytics.grid(row=7, column=0, columnspan=2)

        label_afile = tk.Label(cfgmen, text="Analysis file:")
        label_afile.grid(row=8, column=0, sticky=tk.W)
        entry_afile = tk.Entry(cfgmen, width=40)
        entry_afile.grid(row=8, column=1, sticky=tk.W)

        label_arecfile = tk.Label(cfgmen, text="Output file:")
        label_arecfile.grid(row=9, column=0, sticky=tk.W)
        entry_arecfile = tk.Entry(cfgmen, width=40)
        entry_arecfile.grid(row=9, column=1, sticky=tk.W)

        def _updopt():
            if standvar.get() != 0:
                entry_stan_ping.config(state=tk.NORMAL)
                entry_stan_up.config(state=tk.NORMAL)
                entry_stan_down.config(state=tk.NORMAL)
            else:
                entry_stan_ping.config(state=tk.DISABLED)
                entry_stan_up.config(state=tk.DISABLED)
                entry_stan_down.config(state=tk.DISABLED)

        standvar = tk.IntVar()
        label_standards = tk.Label(cfgmen, text="Standards:")
        label_standards.grid(row=10, column=0, sticky=tk.W)
        button_standards = tk.Checkbutton(cfgmen, text="Enable",
                                          variable=standvar,
                                          command=_updopt)
        button_standards.grid(row=10, column=1, sticky=tk.W)

        label_stan_ping = tk.Label(cfgmen, text="Ping standard:")
        label_stan_ping.grid(row=11, column=0, sticky=tk.W)
        entry_stan_ping = tk.Entry(cfgmen, width=5)
        entry_stan_ping.grid(row=11, column=1, sticky=tk.W)

        label_stan_up = tk.Label(cfgmen, text="Upload standard (Mbps):")
        label_stan_up.grid(row=12, column=0, sticky=tk.W)
        entry_stan_up = tk.Entry(cfgmen, width=6)
        entry_stan_up.grid(row=12, column=1, sticky=tk.W)

        label_stan_down = tk.Label(cfgmen, text="Download standard (Mbps):")
        label_stan_down.grid(row=13, column=0, sticky=tk.W)
        entry_stan_down = tk.Entry(cfgmen, width=6)
        entry_stan_down.grid(row=13, column=1, sticky=tk.W)

        _updopt()


    def resnet(self):
        # If only ResNet would've made this page easier to find,
        # this option wouldn't be needed.
        webbrowser.open("http://und.edu/web-support/request.cfm")

    # here we go... avoid this code.  it's bad.
    def init_gui(self):
        self.root.title("Internet Speed Tester")

        self.status_label = tk.Label(self.root, text="Status: stopped")
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
        self.location_entry.insert(0, LOCATION)

        self.makefile_button = tk.Button(self.root, text="Create analysis file",
                                         command=self.make_analysis_file)
        self.makefile_button.grid(row=3, column=0, columnspan=2,
                                  sticky=tk.W)
        self.upload_button = tk.Button(self.root, text="Upload",
                                       command=self.upload_data)
        self.upload_button.grid(row=3, column=1, sticky=tk.W)

        self.thread_status = tk.Label(self.root, text="Thread status:")
        self.thread_status.grid(row=4, column=0, columnspan=3, sticky=tk.W)
        self.last_test_label = tk.Label(self.root, text="Last: ")
        self.last_test_label.grid(row=5, column=0, columnspan=3, sticky=tk.W)

        self.avg_test_label = tk.Label(self.root, text="Avg.: ")
        self.avg_test_label.grid(row=6, column=0, columnspan=3, sticky=tk.W)

        self.config_button = tk.Button(self.root, text="Edit configuration",
                                       command=self.edit_config)
        self.config_button.grid(row=7, column=0, sticky=tk.W)

        self.resnet_button = tk.Button(self.root, text="ResNet",
                                       command=self.resnet)
        self.resnet_button.grid(row=7, column=1, sticky=tk.W)

if __name__ == '__main__':
    stg = SpeedTesterGUI()
