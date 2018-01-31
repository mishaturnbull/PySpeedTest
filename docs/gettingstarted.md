# Getting Started

## Windows

[Download the program from here][windows_master] by clicking on the `.exe` file.

Put that file somewhere you'll remember it, then double-click it to run.  The program will automatically create a file called `config.ini` containing configuration defaults.  From there, you can continue to use the program as you wish.

## Mac

Problem here.  I don't have a Mac, so I can't test anything on them.  I also can't compile single-file builds for them either.  You'll be stuck executing the Python source until I can find a better solution -- which I am working on.  In the mean time, you can do this:

1. Download the zip file from the left side of the screen
2. Unzip it
3. Open a terminal window in the extracted directory
4. Type `python gui.py` 

## Linux/\*nix

Any distro that comes with Python should be able to run this no problem.  If you're running it on a headless machine such as a Raspberry Pi, I'd recommend checking out the [`one-file`][onefile_branch] for something that might suit your needs more (unless you're using X11 forwarding).  To install the GUI version on a linux machine, run these commands:

```bash
git clone https://github.com/mishaturnbull/PySpeedTest.git PySpeedTest
cd PySpeedTest
python3 gui.py
```



[windows_master]: https://github.com/mishaturnbull/PySpeedTest/releases/latest "Latest release for Windows x64"
[onefile_banch]: https://github.com/mishaturnbull/PySpeedTest/tree/one-file "Terminal version"