# -*- coding: utf-8 -*-

import time as tm
from pyspeedtest import pretty_speed

from settings import REC_FILE, ANALYZE_FILE, ANALYTICS_REC_FILE, \
                     STANDARDS_ENABLE, STANDARD_PING, STANDARD_DOWN, \
                     STANDARD_UP, LOCATION, FORCE_SERVER

RECORD_FILE_NAME = REC_FILE
if ANALYZE_FILE != 'None':
    RECORD_FILE_NAME = ANALYZE_FILE

def avg(l):
    """Average of a list."""
    return round(sum(l) / float(len(l)), 2)

def run_analytics():

    with open(RECORD_FILE_NAME, 'r') as record:
        lines = record.readlines()

    if len(lines) <= 0:
        # not sure how it would be less than 0, but hey... error checking.
        raise ValueError("There must be data present to perform an"
                         " analysis!")

    records = {"time": [], "locs": [], "ping": [], "down": [], "up": []}
    fails, totaltries = 0, 0

    for line in lines:
        try:
            time, loc, ping, down, up = line.split(", ")
            records['time'].append(tm.strptime(time, "%a %b %d %w %Y at %H:%M:%S"))
            records['locs'].append(loc)
            records['ping'].append(float(ping))
            records['down'].append(float(down))
            records['up'].append(float(up))
        except ValueError:
            # it was a connection error
            fails += 1
        totaltries += 1

    statlines = []

    # meta
    statlines.append(" " * 10 + " INTERNET SPEED REPORT")
    statlines.append("     Location: " + LOCATION)
    statlines.append("Time window: beginning " + tm.asctime(records['time'][0]))
    statlines.append("             end       " + tm.asctime(records['time'][-1]))
    statlines.append("Server specified: " + str(FORCE_SERVER))

    statlines.append("\n")

    # pings
    statlines.append(" " * 10 + "  PING STATISTICS  " + " " * 10)
    statlines.append("Fastest ping: " + str(min(records['ping'])) + " ms")
    statlines.append("Slowest ping: " + str(max(records['ping'])) + " ms")
    statlines.append("Average ping: " + str(avg(records['ping'])) + " ms")

    statlines.append("\n")

    # download
    statlines.append(" " * 10 + "DOWNLOAD STATISTICS" + " " * 10)
    statlines.append("Fastest download: " + pretty_speed(max(records['down'])))
    statlines.append("Slowest download: " + pretty_speed(min(records['down'])))
    statlines.append("Average download: " + pretty_speed(avg(records['down'])))

    statlines.append("\n")

    # upload
    statlines.append(" " * 10 + " UPLOAD STATISTICS " + " " * 10)
    statlines.append("Fastest upload: " + pretty_speed(max(records['up'])))
    statlines.append("Slowest upload: " + pretty_speed(min(records['up'])))
    statlines.append("Average upload: " + pretty_speed(avg(records['up'])))

    statlines.append("\n")

    if STANDARDS_ENABLE:
        print("Standards!" + str(STANDARDS_ENABLE))

        statlines.append(" " * 10 + " OUT-OF-STANDARDS" + " " * 10)

        # below standard rates
        statlines.append("Total connection attempts: " + str(totaltries))
        statlines.append("Total failed connection attempts: " + str(fails))
        statlines.append("Total successful connection attempts: " +
                         str(totaltries - fails))
        statlines.append("Percentage of failed connections: " +
                         str(round(fails / totaltries, 4) * 100) + "%")

        statlines.append("")

        n_ping_above_std = 0
        for ping in records['ping']:
            if ping > STANDARD_PING:
                n_ping_above_std += 1
        statlines.append("Number of ping times above " + str(STANDARD_PING) + " ms: " +
                         str(n_ping_above_std))
        p_ping_above_std = round(n_ping_above_std / totaltries, 3)
        statlines.append("Percentage of ping times below standard: " +
                         str(p_ping_above_std * 100) + "%")
        statlines.append("Hours/day ping time is below standard: " +
                         str(round(p_ping_above_std * 24, 1)) + " hours")
        statlines.append("")

        n_down_below_std = 0
        for down in records['down']:
            if down < STANDARD_DOWN:
                n_down_below_std += 1
        statlines.append("Number of download speeds below " + pretty_speed(STANDARD_DOWN) + ": " +
                         str(n_down_below_std))
        p_down_below_std = round(n_down_below_std / totaltries, 3)
        statlines.append("Percentage of download speeds below standard: " +
                         str(p_down_below_std * 100) + "%")
        statlines.append("Hours/day download speed is below standard: " +
                         str(round(p_down_below_std * 24, 1)) + " hours")
        statlines.append("")

        n_up_below_std = 0
        for up in records['up']:
            if up < STANDARD_UP:
                n_up_below_std += 1
        statlines.append("Number of upload speeds below " + pretty_speed(STANDARD_UP) + ": " +
                         str(n_up_below_std))
        p_up_below_std = round(n_up_below_std / totaltries, 3)
        statlines.append("Percentage of upload speeds below standard: " +
                         str(p_up_below_std * 100) + "%")
        statlines.append("Hours/day upload speed is below standard: " +
                         str(round(p_up_below_std * 24, 1)) + " hours")
        statlines.append("\n")

    with open(ANALYTICS_REC_FILE, 'w') as out:
        out.writelines('\n'.join(statlines))
