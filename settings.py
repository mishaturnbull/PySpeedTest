# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:02:00 2018

@author: Misha
"""

import configparser

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