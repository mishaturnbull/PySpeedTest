# -*- coding: utf-8 -*-

import time as tm
from matplotlib import pyplot as plotter

with open("speed_record.txt", 'r') as record:
    lines = record.readlines()[4:]  # get rid of the header

records = {"time": [], "ping": [], "down": [], "up": []}
fails, totaltries = 0, 0

MAX_PING = 25
MIN_DOWN = 20 * 1000000
MIN_UP = 20 * 1000000

for line in lines:
    try:
        time, ping, down, up = line.split(", ")
        ftime = tm.strptime(time, "%a %b %d %Y at %H:%M:%S")
        records['time'].append(ftime.tm_hour + (ftime.tm_min / 60.0))
        records['ping'].append(float(ping))
        records['down'].append(float(down))
        records['up'].append(float(up))
    except ValueError:
        # it was a connection error
        fails += 1
    totaltries += 1

pingchart = plotter.scatter(records['time'], records['ping'])
downchart = plotter.scatter(records['time'], records['down'])
upchart = plotter.scatter(records['time'], records['up'])

print(downchart)
print(upchart)
