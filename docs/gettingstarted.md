[Back to main page](index.html)

# Getting Started

## Windows

[Download the program from here][windows_master] by clicking on the `.exe` file.

Put that file somewhere you'll remember it, then double-click it to run.  The program will automatically create a file called `config.ini` containing configuration defaults.  From there, you can continue to use the program as you wish.

## Mac

***UPDATE 2018/02/13***:  I tested it on a friend's Mac and found [more issues](https://github.com/mishaturnbull/PySpeedTest/issues/15).  It is hard to run right now.  I am working on making easier to run.

Problem here.  I don't have a Mac, so I can't test anything on them.  I also can't compile single-file builds for them either.  You'll be stuck executing the Python source until I can find a better solution -- which I am working on.  In the mean time, you can do this:

1. Download the zip file from the left side of the screen
2. Unzip it
3. Double-click the file called `mac_run_this.command`.  You may have to allow apps from unidentified developers. 

## Linux/\*nix

Any distro that comes with Python should be able to run this no problem.  If you're running it on a headless machine such as a Raspberry Pi, I'd recommend checking out the [`one-file`][onefile_branch] for something that might suit your needs more (unless you're using X11 forwarding).  To install the GUI version on a linux machine, run these commands:

```bash
git clone https://github.com/mishaturnbull/PySpeedTest.git PySpeedTest
cd PySpeedTest
python3 gui.py
```



[windows_master]: https://github.com/mishaturnbull/PySpeedTest/releases/latest "Latest release for Windows x64"
[onefile_banch]: https://github.com/mishaturnbull/PySpeedTest/tree/one-file "Terminal version"