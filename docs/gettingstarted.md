[Back to main page](index.html)

# Getting Started

## Windows

[Download the program from here][windows_master] by clicking on the `.exe` file.

Put that file somewhere you'll remember it, then double-click it to run.  The program will automatically create a file called `config.ini` containing configuration defaults.  From there, you can continue to use the program as you wish.

## Mac

***UPDATE 2018/03/21***:  Take a look at [this note about Macs][mac] for more details.  It's iffy.

Download the file named `PySpeedTest_vX.Y.Z_mac.app.zip`, put it somewhere, and double-click it.  Weird warnings may appear.  Look at the [note][mac] for details. 

The program will automatically create two files in the same folder as it is located: `speed_record.ilog`, a record of the internet speeds, and `config.ini`.  The speed record filename can be changed through the program's settings menu, but at this time the configuration file's name cannot be changed.

## Linux/\*nix

Any distro that comes with Python should be able to run this no problem.  If you're running it on a headless machine such as a Raspberry Pi, I'd recommend checking out the [`one-file`][onefile_branch] for something that might suit your needs more (unless you're using X11 forwarding).  To install the GUI version on a linux machine, run these commands:

```bash
git clone https://github.com/mishaturnbull/PySpeedTest.git PySpeedTest
cd PySpeedTest
python3 gui.py
```


[mac]: https://mishaturnbull.github.io/PySpeedTest/macs.html
[windows_master]: https://github.com/mishaturnbull/PySpeedTest/releases/latest "Latest release for Windows x64"
[onefile_banch]: https://github.com/mishaturnbull/PySpeedTest/tree/one-file "Terminal version"