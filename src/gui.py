# -*- coding: utf-8 -*-
#flake8: noqa: E402
"""
Graphical user interface for speed test.

Hopefully useful.
"""

# now, we have to import the dependency tester to make sure required modules
# are present and if not install them for us
from dependencies import download_dependencies
download_dependencies()  # pretty please work


# import the rest of the code
from main import test_once
from uploadclient import Uploader
from analytics import run_analytics
from autoupdate import has_update, download_update
from settings import REC_FILE, LOCATION, FREQ, VERBOSITY, FORCE_SERVER, \
                     ANALYZE_FILE, ANALYTICS_REC_FILE, STANDARDS_ENABLE, \
                     STANDARD_PING, STANDARD_UP, STANDARD_DOWN, UPLOAD_URLS, \
                     UPLOAD_PORT, CONFIG_FILE_NAME, parser
from persistence import resource_path

# makes the test display easier to read
from pyspeedtest import pretty_speed

# showing errors
import errors

# tcl/tk -- used for building GUI
# messagebox -- neat little popup window
try:
    import tkinter as tk
    import tkinter.messagebox as messagebox
except ImportError:
    import Tkinter as tk
    import tkMessageBox as messagebox

# for the Resnet button
import webbrowser

# py2/py3
import sys

# for running the speedtester thread in the background
import threading

# recordng time
import time

# letters
import string

BLOCK_EXIT_CONDITIONS = ['testing', 'waiting']
BLOCK_UPLOAD_CONDITIONS = ['testing', 'writing', 'paused']

# background thread for running speed tests
class SpeedTesterThread(threading.Thread):
    """
    Background thread for running speed tests.
    """

    def __init__(self, handler):
        """
        Instantiate thread handler.
        """

        threading.Thread.__init__(self)

        # used to pass the last result to the GUI handler for analysis/display
        self.last_result = {'ping': 0, 'up': 0, 'down': 0}

        # GUI tells us whether to stop or not
        self.stoprequest = threading.Event()

        # GUI handler itself
        self.handler = handler

        # program is closing, stop now
        self.exit = False

    def run(self):
        """
        Run the thread (or don't)
        """

        # tell the user we're running
        self.handler.thread_status.config(text="Thread status: alive")

        try:
            while not self.exit:
                # if the stop request is set, we want to stop.  so, run
                # while it's not
                while not self.stoprequest.isSet():
                    print(self.handler)

                    # tell user we're testing
                    self.handler.thread_status.config(
                        text="Thread status: testing")

                    # run the speed test
                    newline, time_diff, self.last_result = test_once(
                        self.handler.location_entry.get())

                    # tell the user we're now outputting the results
                    self.handler.thread_status.config(
                        text="Thread status: writing results")

                    # write the results to the specified file
                    with open(REC_FILE, 'a') as record:
                        record.write(newline)

                    # tell the handler we're done so it can update the
                    # display
                    self.handler.update_statistics()

                    # check again for stop request here -- otherwise, we'll
                    # wait to the next test unnecessarily
                    if not self.stoprequest.isSet():
                        self.handler.thread_status.config(
                            text="Thread status: waiting")
                        time.sleep(time_diff)
                    else:
                        self.handler.thread_status.config(
                            text='Thread status: paused')
                        continue
                self.handler.status_label.config(text="Status: stopped")
                self.handler.thread_status.config(
                    text="Thread status: dead")
                time.sleep(0.5)  # let's not be too hard on the system
        except RuntimeError:
            # most likely, it's this one:
            # RuntimeError: main thread is not in main loop
            # basically, means that the program was closed without properly
            # stopping the thread.  darned users :)
            # all we have to do here is stop the loop (done) and exit
            # safely...
            self.exit = True
            self.stoprequest.set()
            return

    def join(self, timeout=None):
        # set the stop request so next time the test starts/stops we'll exit
        self.stoprequest.set()
        super(SpeedTesterThread, self).join(timeout)


class SpeedTesterGUI(object):
    """
    Speed tester GUI object
    """

    def __init__(self):
        """
        Instantiate the GUI menu.  Runs automatically.
        """

        # root window
        self.root = tk.Tk()

        # set defaults
        self.location = "-- ENTER LOCATION --"
        self.lasttest = {'ping': 0, 'up': 0, 'down': 0}
        self.avg = {'ping': 0, 'up': 0, 'down': 0}
        self.ntests = 0

        # instantiate the speed tester background thread
        self.thread = SpeedTesterThread(self)

        # instantiate the upload UI
        self.uploader = Uploader(self)

        # build and start the GUI
        self.init_gui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # this has to be below the init_gui() method:
        # https://github.com/mishaturnbull/PySpeedTest/issues/6
        self.update_routine()

        try:
            self.root.mainloop()
        except Exception as exc:
            if sys.version_info[0] == 2:
                messagebox.showerror("PySpeedTest Broke",
                                     exc.message)
            elif sys.version_info[0] == 3:
                messagebox.showerror("PySpeedTest Broke",
                                     sys.exc_info()[0])

    def update_routine(self):
        # check for updates, if available, ask to install them
        # after downloading, ask user if they want to close the program
        try:
            update_available = has_update()
        except Exception:
            # can't update with no connection!
            # not a big problem here, fail silently and move on.
            # annoying to have a popup every time you start the program
            # that says you don't have a connection, especially for a
            # feature that's not vital to program operation
            update_available = False

        if update_available:

            msgstring = ("An update has been detected.  Would you like "
                         "to download it?")
            want_update = messagebox.askyesno("Update", msgstring)
            if want_update:
                # new_version is just the filename
                # of the freshly downloaded program
                new_version = download_update()

                msgstring = ("The newest version has been downloaded: {}"
                             " Would you like to close this version now?"
                             " The new version will not open"
                             " automatically").format(resource_path(
                                 new_version))
                want_close = messagebox.askyesno("Update", msgstring)

                if want_close:
                    # all we can do here is close the program.
                    # hopefully, the user finds their way to the new
                    # version...
                    # stop the thread, wait half a second, close...
                    # hope for the best.  worst case, users get a popup
                    # about can't close the program (see self.close())
                    # and nothing more happens
                    self.stop()
                    self.root.after(500, self.close)

    def update_statistics(self):
        """
        Updates the statistics display on the GUI menu.

        Responsible for keeping track of rolling averages and last tests.
        Called directly by the tester thread.
        """

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

        # create new format strings from computed averages/last test
        # \u2191 is an up arrow
        # \u2193 is a down arrow
        last_str = u"Last: {ping}ms / {up}\u2191 / {down}\u2193".format(
            ping=self.lasttest['ping'],
            up=pretty_speed(self.lasttest['up']),
            down=pretty_speed(self.lasttest['down']))
        avg_str = u"Avg: {ping}ms / {up}\u2191 / {down}\u2193".format(
            ping=round(self.avg['ping'], 2),
            up=pretty_speed(self.avg['up']),
            down=pretty_speed(self.avg['down']))

        # apply changes
        self.last_test_label.config(text=last_str)
        self.avg_test_label.config(text=avg_str)

    def start(self):
        """
        Start the tester thread.

        https://github.com/mishaturnbull/PySpeedTest/issues/4
        """
        self.lasttest = {'ping': 0, 'up': 0, 'down': 0}
        self.avg = {'ping': 0, 'up': 0, 'down': 0}
        self.ntests = 0
        self.status_label.config(text="Status: running")
        if self.thread.stoprequest.isSet():
            self.thread.stoprequest.clear()
        else:
            self.thread.start()

    def stop(self):
        """
        Stop the tester thread.

        Should not cause the program to hang.
        """
        self.status_label.config(text="Status: stopping")
        self.thread.stoprequest.set()
        self.thread.exit = True

    def close(self):
        """
        Close action
        """
        self.thread.exit = True
        self.stop()

        self.root.destroy()

    def make_analysis_file(self):
        """
        Create the statistical analysis file.
        """
        try:
            run_analytics()
        except Exception as exc:
            errors.display_error(exc, False)

    def upload_data(self):
        """
        Upload data to the server.

        Requires a network connection (duh).
        """
        status = self.thread_status.cget("text").lower()
        if any(s in status for s in BLOCK_UPLOAD_CONDITIONS):
            messagebox.showerror("Upload",
                                 "Unable to upload right now.  Try again"
                                 " in a moment, this issue is temporary.")
            return

        self.uploader.build_window()
        self.uploader.establish_connection()
        self.uploader.send_data()

    def edit_config(self):
        """
        Configuration edit menu.
        Shouldn't all be in one function, but oh well.
        """

        cfgmen = tk.Toplevel(self.root)
        cfgmen.wm_title("Configuration")

        def set_vars():
            """
            The 'Apply' button.

            https://github.com/mishaturnbull/PySpeedTest/issues/5
            """
            parser.set('Speedtester', 'rec_file', entry_recfile.get())
            parser.set('Speedtester', 'freq', entry_freq.get())
            parser.set('Speedtester', 'verbosity', entry_verbosity.get())
            parser.set('Speedtester', 'force_server', entry_server.get())
            parser.set('Speedtester', 'location', entry_location.get())
            parser.set('Analytics', 'analyze_file', entry_afile.get())
            parser.set('Analytics', 'analytics_rec_file', entry_arecfile.get())
            parser.set('Analytics', 'standards_enable', str(bool(standvar.get())))
            parser.set('Analytics', 'standard_ping', entry_stan_ping.get())
            parser.set('Analytics', 'standard_up', entry_stan_up.get())
            parser.set('Analytics', 'standard_down', entry_stan_down.get())
            parser.set('Upload', 'port', entry_upload_port.get())

            letters = string.ascii_lowercase
            urls = entry_upload_url.get()
            urls = [s.strip() for s in urls.split(',')]
            for i in range(len(urls)):
                parser.set("UploadURLs", letters[i], urls[i])

            with open(CONFIG_FILE_NAME, 'w') as configfile:
                parser.write(configfile)

            ## FIXME: workaround for issue #5.  NOT A FIX!
            messagebox.showwarning("Configuration", "You will need to restart"+
                                   " the program for changes to take effect!")

        def refresh():
            """
            The 'Defaults' button.
            """
            entry_recfile.delete(0, 'end')
            entry_recfile.insert(0, REC_FILE)

            # Set the location field to be the value of the location field
            # in the main menu

            entry_location.delete(0, 'end')
            entry_location.insert(0, self.location_entry.get())

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

            entry_upload_url.delete(0, 'end')
            entry_upload_url.insert(0, ','.join(UPLOAD_URLS))

            entry_upload_port.delete(0, 'end')
            entry_upload_port.insert(0, str(UPLOAD_PORT))


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
            """
            Standards enable/disable toggle greyout fields shortcut.
            """
            if standvar.get() != 0:
                entry_stan_ping.config(state=tk.NORMAL)
                entry_stan_up.config(state=tk.NORMAL)
                entry_stan_down.config(state=tk.NORMAL)
            else:
                entry_stan_ping.delete(0, 'end')
                entry_stan_ping.insert(0, '0')
                entry_stan_up.delete(0, 'end')
                entry_stan_up.insert(0, '0')
                entry_stan_down.delete(0, 'end')
                entry_stan_down.insert(0, '0')
                entry_stan_ping.config(state=tk.DISABLED)
                entry_stan_up.config(state=tk.DISABLED)
                entry_stan_down.config(state=tk.DISABLED)

        standvar = tk.IntVar()
        label_standards = tk.Label(cfgmen, text="Standards:")
        label_standards.grid(row=10, column=0, sticky=tk.W)
        button_standards = tk.Checkbutton(cfgmen, text="Enabled",
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

        label_sec_upload = tk.Label(cfgmen, text="===== UPLOAD SETTINGS =====")
        label_sec_upload.grid(row=14, column=0, columnspan=2)

        label_upload_url = tk.Label(cfgmen, text="Upload URL:")
        label_upload_url.grid(row=15, column=0, sticky=tk.W)
        entry_upload_url = tk.Entry(cfgmen, width=40)
        entry_upload_url.grid(row=15, column=1, sticky=tk.W)

        label_upload_port = tk.Label(cfgmen, text="Upload port:")
        label_upload_port.grid(row=16, column=0, sticky=tk.W)
        entry_upload_port = tk.Entry(cfgmen, width=7)
        entry_upload_port.grid(row=16, column=1, sticky=tk.W)

        _updopt()
        refresh()


    def resnet(self):
        """
        Open your web browser to the ResNet support ticket page.
        """
        # If only ResNet would've made this page easier to find,
        # this option wouldn't be needed.
        webbrowser.open("http://und.edu/web-support/request.cfm")

    # here we go... avoid this code.  it's bad.
    def init_gui(self):
        """
        Make it all look pretty (not)
        """
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

    try:
        stg = SpeedTesterGUI()
    except Exception as exc:
        errors.display_error(exc, raise_when_done=False)
