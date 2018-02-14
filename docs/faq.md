[Back to main page](index.html)

# Table of contents
1. [Problems](#problems)  
    1.1 [Why can't I close the program?](#why-cant-i-close-the-program)

# Problems

## Why can't I close the program?

Typically, when you try to close the program, it will display an error message and say it can't be closed at this time.  This error message was built in very much intentionally to help prevent leaving programs running in the background.  The speed testing is conducted in a background "thread" -- that is, a kind of "helper program" -- controlled by the graphical menu.  While the tester thread is either running its test or waiting for the next one, it doesn't accept any instruction from the menu.  The only times it checks for input is immediately before and immediately after running tests.  This means that if you close the menu without stopping the thread first, it has nothing to tell it to stop.  If you do this repeatedly, you now have 10 test threads running on your computer.  And you can't stop them.  This is bad.

All you have to do to not get this is click `Stop` and wait for the display `Thread status: dead` before closing the program.