# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:02:00 2018

@author: Misha
"""

import configparser

EMERGENCY_DEFAULT = """
[Speedtester]
rec_file = speed_record.ilog
location = Wherever
freq = 0.5
verbosity = 3
force_server = None

[Analytics]
analyze_file = None
analytics_rec_file = report.txt
standards_enable = False
standard_ping = 0.0
standard_down = 0.0
standard_up = 0.0

[CSV]
csv_input_file = None
csv_output_file = Internet_speed_record.csv
csv_clear_infile = False
"""

try:
    f = open('config.ini')
    f.close()
except FileNotFoundError:
    with open('config.ini', 'w') as configfile:
        configfile.write(EMERGENCY_DEFAULT)

parser = configparser.ConfigParser()
parser.read("config.ini")

REC_FILE = parser['Speedtester']['rec_file']
LOCATION = parser['Speedtester']['location']
FREQ = float(parser['Speedtester']['freq'])
VERBOSITY = int(parser['Speedtester']['verbosity'])
server = parser['Speedtester']['force_server']
FORCE_SERVER = None if server == 'None' else server

ANALYZE_FILE = parser['Analytics']['analyze_file']
ANALYTICS_REC_FILE = parser['Analytics']['analytics_rec_file']
STANDARDS_ENABLE = parser['Analytics']['standards_enable']
STANDARD_PING = float(parser['Analytics']['standard_ping'])
STANDARD_DOWN = float(parser['Analytics']['standard_down'])
STANDARD_UP = float(parser['Analytics']['standard_up'])

CSV_INPUT_FILE = parser['CSV']['csv_input_file']
CSV_OUTPUT_FILE = parser['CSV']['csv_output_file']
CSV_CLEAR_INFILE = parser['CSV']['csv_clear_infile']

UPLOAD_URL = parser['UPLOAD']['url']
UPLOAD_PORT = int(parser['UPLOAD']['port'])