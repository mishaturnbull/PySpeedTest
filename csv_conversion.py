# -*- coding: utf-8 -*-
import time

from settings import CSV_INPUT_FILE, CSV_OUTPUT_FILE, CSV_CLEAR_INFILE, REC_FILE

def reformat_date(datefield):
    date = time.strptime(datefield, "%a %b %d %w %Y at %H:%M:%S")
    out = time.strftime("%Y,%m,%d,%w,%H,%M,%S,", date)
    timeidx = (date.tm_sec + date.tm_min*60 + date.tm_hour*3600)/86400 + \
        date.tm_wday
    out += str(timeidx) + ',-0500'
    return out

readfilename = REC_FILE
if CSV_INPUT_FILE:
    readfilename = CSV_INPUT_FILE

with open(readfilename, 'r') as record:
    lines = record.readlines()[4:]

newlines = []
i = 0

for line in lines:

    # first, split on the commas and strip whitespace
    line = line.split(', ')
    line = [field.strip() for field in line]
    fields = []
    i += 1

    fields.append(reformat_date(line[0]))

    # check the length of `line`.  if 3, connection error; if 5, normal
    if len(line) == 3:
        fields.append(line[1])
        # connection error
        if "downloaded" in line[1]:
            # download error
            fields.append("Download failure")
        elif "uploaded" in line[1]:
            # upload error
            fields.append("Upload failure")
        else:
            # total error
            fields.append("Connection failure")
    elif len(line) == 5:
        # normal
        fields.extend(line[1:])
    else:
        print(line)
        print("Critical: The above line is misformatted.  No data has been")
        print("          written to {} or cleared from {}.".format())
        assert False, "Misformatted line"

    line = ','.join(fields) + '\n'
    newlines.append(line)

with open(CSV_OUTPUT_FILE, 'w') as datafile:
    datafile.writelines(newlines)

if CSV_CLEAR_INFILE:
    with open(readfilename, 'w') as clearfile:
        clearfile.write('')
