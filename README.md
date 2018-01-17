# Python Internet Speed Test

This is a small, lightweight utility that tests the Internet connection at set intervals.  I wrote it to prove to the people who manage my Internet that it's ***really*** bad.  It takes periodic (or not-so-periodic) samples of your Internet speed.  Statistics recorded are upload speed, download speed, ping time, and if something fails reason for failure.  



## Configuring output

By default, running `main.py` will produce a file called `speed_record.ilog` (`ilog` for "internet log") recording the date, time, location (user-specified), ping time, upload, and download speeds.  Each record takes up one line and is separated by a single newline character.  