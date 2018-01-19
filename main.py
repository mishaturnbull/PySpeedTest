# -*- coding: utf-8 -*-

"""
Main program for PySpeedMonitor.

Monitors internet speed at set intervals.  Can be configured through the
accompanying `settings.py` file.
"""

import datetime
import time
import sys

from settings import REC_FILE, LOCATION, FREQ, VERBOSITY, FORCE_SERVER

try:
    import pyspeedtest
except ModuleNotFoundError:
    print("Critical: Required module PySpeedTest not found.")
    print("          Running this in terminal/cmd will probably fix it:")
    print("          pip install pyspeedtest")
    sys.exit(1)

# lazy man's debugging
def dprint(level, msg):
    """Debug printer.  Args are [level], [message]."""
    if VERBOSITY >= level:
        print(msg)

while True:

    st = pyspeedtest.SpeedTest()
    
    # Yes, I know this is ultra-bad practice.  I'm overriding the setting
    # without editing the source of pyspeedtest.
    st._host = FORCE_SERVER # pylint: disable=W0212

    a = datetime.datetime.now()
    curtime = a.strftime("%a %b %d %w %Y at %H:%M:%S")

    dprint(2, "About to test at " + curtime)
    try:
        dprint(3, "About to ping...")
        ping = round(st.ping(), 2)
        dprint(3, "About to download...")
        down = round(st.download(), 1)
        dprint(3, "About to upload...")
        up = round(st.upload(), 1)
        newline = ", ".join([curtime, LOCATION, str(ping), str(down), str(up)]) \
                  + '\n'
    except Exception as e:
        dprint(1, "It didn't work!  Joining error line...")
        newline = ", ".join([curtime, LOCATION, e.__repr__()]) + '\n'

    dprint(2, "Test completed, result:")
    dprint(1, newline)
    with open(REC_FILE, 'a') as record:
        record.write(newline)

    b = datetime.datetime.now()

    t = (FREQ * 60) - (b - a).total_seconds()
    if t < 0:
        t = 0  # hope we catch up eventually

    time.sleep(t)
