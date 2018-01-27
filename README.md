# Python Internet Speed Test

This is a small, lightweight utility that tests the Internet connection at set intervals.  I wrote it to prove to the people who manage my Internet that it's ***really*** bad.  It takes periodic (or not-so-periodic) samples of your Internet speed.  Statistics recorded are upload speed, download speed, ping time, and if something fails reason for failure.  

## Quick start

Download the executable from [here][0], put it somewhere you'll remember, run it and click the `Start` button.  If you want to make my life a bit better, before you click start, type in the `Location` field where you are (be descriptive, but brief.  For example, here, I write "McVey 3rd north", not "404 Stanford Road, Grand Forks, ND 58202 ...").  After a little while, click the `Stop` button, and then the `Upload` button.  Repeat until you don't want to anymore.

Windows users may receive SmartScreen warnings; click `Run Anyways` if it's available, if not, click `More Info` then it should show up.  I promise this doesn't do anything bad.  Unless you're ResNet.

## Updating

As of [version 0.4.3][1], the program will check for updates on launch.  If an updated version is found, it will prompt user for a yes/no answer to download the updated version or not.  At present, the auto-updater will not remove the outdated version, but this could be implemented in the future.

## Configuration
If you want to change your settings, launch the program and click the `Edit Configuration` button.  This will spawn a pop-up window with empty fields (working on it!). Click `Refresh` in the top right corner to populate the fields with the current values.  Edit as you wish, then click `Apply`.  

[0]: https://github.com/mishaturnbull/PySpeedTest/releases	"Latest Release"
[1]: https://github.com/mishaturnbull/PySpeedTest/releases/v0.4.3	"Version 0.4.3"