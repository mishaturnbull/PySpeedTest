# -*- coding: utf-8 -*-


try:
    import pyspeedtest
except ModuleNotFoundError:
    import os
    os.system('pip install pyspeedtest')
    import pyspeedtest

import datetime
import time

record_file = "speed_record_new.txt"

#     "-----------------"
LOC = "Outside 301A"

while True:

    st = pyspeedtest.SpeedTest()

    a = datetime.datetime.now()
    curtime = a.strftime("%a %b %d %w %Y at %H:%M:%S")

    print("About to test at " + curtime)
    try:
        print("About to ping...")
        ping = round(st.ping(), 2)
        print("About to download...")
        down = round(st.download(), 1)
        print("About to upload...")
        up = round(st.upload(), 1)
        newline = ", ".join([curtime, LOC, str(ping), str(down), str(up)]) \
                  + '\n'
    except Exception as e:
        print("It didn't work!  Joining error line...")
        newline = ", ".join([curtime, LOC, e.__repr__()]) + '\n'

    print("Test completed, result:")
    print(newline)
    with open(record_file, 'a') as record:
        record.write(newline)

    b = datetime.datetime.now()

    t = (.5 * 60) - (b - a).total_seconds()
    if t < 0:
        t = 0  # hope we catch up eventually

    time.sleep(t)  # every 5min
