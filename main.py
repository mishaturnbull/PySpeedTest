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

def make_speedtest_object():
    speed_tester = pyspeedtest.SpeedTest()

    # Yes, I know this is ultra-bad practice.  I'm overriding the setting
    # without editing the source of pyspeedtest.
    speed_tester._host = FORCE_SERVER # pylint: disable=W0212

    return speed_tester


def test_once():
    speed_tester = make_speedtest_object()

    time_a = datetime.datetime.now()
    curtime = time_a.strftime("%a %b %d %w %Y at %H:%M:%S")

    dprint(2, "About to test at " + curtime)
    try:
        dprint(3, "About to ping...")
        ping = round(speed_tester.ping(), 2)
        dprint(3, "About to download...")
        down = round(speed_tester.download(), 1)
        dprint(3, "About to upload...")
        upload_speed = round(speed_tester.upload(), 1)
        newline = ", ".join([curtime, LOCATION, str(ping), str(down), str(upload_speed)]) \
                  + '\n'
    except Exception as exc:
        dprint(1, "It didn't work!  Joining error line...")
        newline = ", ".join([curtime, LOCATION, exc.__repr__()]) + '\n'

    time_b = datetime.datetime.now()

    dprint(2, "Test completed, result:")
    dprint(1, newline)

    time_diff = (FREQ * 60) - (time_b - time_a).total_seconds()
    if time_diff < 0:
        time_diff = 0  # hope we catch up eventually

    return newline, time_diff, {'ping': ping, 'down': down, 'up': upload_speed}


def main():

    while True:
        newline, time_diff, _ = test_once()
        with open(REC_FILE, 'a') as record:
            record.write(newline)
        time.sleep(time_diff)


if __name__ == '__main__':
    main()
