# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:02:00 2018

@author: Misha
"""

################ MAIN PROGRAM SETTINGS ################

######## Name of file to output to:
# No matter the extension, the program writes pure text data and the file can
# be opened and read with any text editor
REC_FILE = "speed_record.ilog"

######## Location to record at:
# The program supports recording speeds at multiple locations (e.g. 'Outside
# room 301' or 'Atrium').   Set the location here.  For prettier outputs,
# don't set a location longer than the guide below.
# Guide:   "-----------------"
LOCATION = "Common Area"

######## Speed test frequency:
# This value specifies how many minutes should elapse between speed tests.
# It is specified in minutes and can be set as a decimal (e.g. 2 is every 2
# minutes, 0.5 is every 30 seconds).  If a test takes longer than `FREQ`
# seconds, the program will start the next test immediately after the first is
# complete.  This behavior will continue until the program catches up to its
# specified testing interval.
FREQ = 0.5

######## Verbosity:
# This value specifies how talkative the program should be.  It scales from
# 0 (run silently with no output) to 3 (tell me everything).  Integers only.
#
# Well I mean decimals *should* work but why would you want do that?
VERBOSITY = 3

################ ANALYTICS PROGRAM SETTINGS ################

######## Name of file to analyze:
# This filename should ONLY be specified if the file you would like to perform
# analytics on is different from the filename specified in the main program's
# record file.
# As an example, if you have multiple record files and would like to analyze
# a different file than the one you most recently created, set this value to
# that filename.
ANALYZE_FILE = None

######## Name of file to output to:
# This is the name of the file that is output by the analytics program.
# It's usually a little easier to set it as a *.txt file.
ANALYTICS_REC_FILE = "report.txt"

######## Speed standards:
# The analytics program can analyze speeds and compare them against a set 
# standard.  An example of using this feature would be if your department
# needs a minimum of 20 Mbit/sec, but isn't getting that, the program will
# tell you what percent of all tests were at or above that standard.

#### Enable:
# Boolean value.  Whether or not to include standards in the report.
STANDARDS_ENABLE = True

#### Ping time:
# Set a maximum requires ping time in milliseconds.
STANDARD_PING = 25.0

#### Download speed:
# Set a minimum download speed in megabit/second.
# FCC defines broadband internet as 25Mbit/s (as of late 2017)
STANDARD_DOWN = 20.0

#### Upload speed:
# Set a minimum upload speed in megabit/second.
# FCC defines broadband internet sa 3Mbit/s (as of late 2017)
STANDARD_UP = 20.0

################ CSV CONVERSION PROGRAM SETTINGS ################

######## Name of file to analyze:
# This filename should ONLY be specified if the file you would like to perform
# conversion on is different from the filename specified in the main program's
# record file.
# As an example, if you have multiple record files and would like to convert
# a different file than the one you most recently created, set this value to
# that filename.
CSV_INPUT_FILE = None

######## Name of file to output to:
# For obvious reasons, I would recommend setting the filetype here to .csv.
CSV_OUTPUT_FILE = "Internet_speed_record.csv"

######## Clear records file on completion:
# This value determines whether or not the program should clear the file
# specified by CSV_INPUT_FILE when the csv conversion and output completes.
# For my use, I left it on, ran the program, copied the data to Excel, and
# processed it there while never even stopping the main program.
CSV_CLEAR_INFILE = False
