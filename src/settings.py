# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:02:00 2018

@author: Misha
"""

# python 2-proofing
import sys

if sys.version_info[0] == 2:
    import ConfigParser as configparser
elif sys.version_info[0] == 3:
    import configparser

import errors

CONFIG_FILE_NAME = "config.ini"

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

[Upload]
port = 11356

[UploadURLs]
a = 172.30.140.181
b = 134.129.156.163
c = mcv156.163.und.nodak.edu
d = 25.3.82.86
"""

try:
    f = open(CONFIG_FILE_NAME)
    f.close()
except IOError:
    with open(CONFIG_FILE_NAME, 'w') as configfile:
        configfile.write(EMERGENCY_DEFAULT)

parser = configparser.ConfigParser()
parser.read("config.ini")

try:
    REC_FILE = parser.get('Speedtester', 'rec_file')
    LOCATION = parser.get('Speedtester', 'location')
    FREQ = float(parser.get('Speedtester', 'freq'))
    VERBOSITY = int(parser.get('Speedtester', 'verbosity'))
    server = parser.get('Speedtester', 'force_server')
    FORCE_SERVER = None if server == 'None' else server
    
    ANALYZE_FILE = parser.get('Analytics', 'analyze_file')
    ANALYTICS_REC_FILE = parser.get('Analytics', 'analytics_rec_file')
    STANDARDS_ENABLE = parser.get('Analytics', 'standards_enable') in ['true', '1', 
                             't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
    STANDARD_PING = float(parser.get('Analytics', 'standard_ping') or 0)
    STANDARD_DOWN = float(parser.get('Analytics', 'standard_down') or 0)
    STANDARD_UP = float(parser.get('Analytics', 'standard_up') or 0)
    
    CSV_INPUT_FILE = parser.get('CSV', 'csv_input_file')
    CSV_OUTPUT_FILE = parser.get('CSV', 'csv_output_file')
    CSV_CLEAR_INFILE = parser.get('CSV', 'csv_clear_infile')
    
    UPLOAD_PORT = int(parser.get('Upload', 'port'))
    url_items = parser.items('UploadURLs')
    UPLOAD_URLS = []
    for key, path in url_items:
        UPLOAD_URLS.append(path)
except (configparser.NoSectionError, configparser.NoOptionError) as exc:
    with open(CONFIG_FILE_NAME, 'w') as conf:
        conf.write(EMERGENCY_DEFAULT)
    
    msg = "\n\nThere was an error loading the configuration file.  Maybe\n"
    msg += "you updated the problem recently?  I restored it to the\n"
    msg += "default state, try loading the program again.\n\n"
    
    errors.display_error(Exception(msg))
