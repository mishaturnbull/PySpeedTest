# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 09:02:00 2018

@author: Misha
"""

######## Name of file to output to:    
# No matter the extension, the program writes pure text data and the file can 
# be opened and read with any text editor
REC_FILE = "speed_record.ilog"   

######## Location to record at: 
# The program supports recording speeds at multiple locations (e.g. 'Outside
# room 301' or 'Atrium').   Set the location here.  For prettier outputs,
# don't set a location longer than the guide below.
# Guide:   "-----------------"         
LOCATION = "wherever"

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
