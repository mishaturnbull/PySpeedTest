[Back to main page](index.html)

# Table of contents
1. [Basic Usage](#basic-usage)  
    1.1 [Running Speed Tests](#running-speed-tests)  
    1.2 [Uploading Results](#uploading-results)  
    1.3 [The ResNet Button](#the-resnet-button)  
    1.4 [Create Analysis File Button](#create-analysis-file-button)  
    1.5 [Example Usage](#example-usage)  

# Basic Usage
<p align="center">
![PySpeedTest](/PySpeedTest/docs/window.png)
</p>

## Running Speed Tests

In order to run speed tests, first, run the program as [described above](## Running), and the little window should pop up.  To start recording the internet speed (which you want to do), click the button that says "Start".

Before you do this, however, enter in the Location field where you are.  This *really* helps me sort through the data and make it useful -- I can't very well tell ResNet that the network speeds are slow in "McVey", but I can tell them it's slow in "McVey 3rd north".  This is surprisingly important.

When you no longer want to run speed tests, click the button that says "Stop".

## Uploading results

***PLEASE PLEASE PLEASE***, when you're done, click the upload button.  That button sends the data you recorded to my computer, which stores it for future analysis.  I can't do anything if I don't get the data you've been collecting.

After the results have been uploaded, they are cleared from your computer.  The main reason for this is to prevent duplicate data -- if, every time you upload data, you upload the same data + a bit more, I will rapidly accumulate vast amounts of identical data that becomes very difficult to filter out.  

## The ResNet Button

Pressing the ResNet button brings you to ResNet's support ticket page.  The sole purpose of this button is because I can never find this page and frequently want to submit tickets when the internet isn't working.  Please don't flood ResNet with tickets for slow internet -- they know about this -- but if it goes down, then let them know.

## Create Analysis File Button

This button creates a summary file based on your current results.  It
[writes a summary to the file](https://github.com/mishaturnbull/PySpeedTest/issues/3)
[specified in the configuration](https://github.com/mishaturnbull/PySpeedTest/issues/5)
without removing the results.  The only gotcha with this feature is that it must be done before uploading: for various reasons, uploading the results clears them from your machine.

## Example Usage

The way I typically use the program is as follows:

1. Notice the internet speed is bad/I want to run tests.
2. Start the program.
3. Upload any previous results (uploading empty data doesn't hurt anything)
4. Tell it where I am (e.g. "McVey 3rd north")
5. Click `Start`
6. Do homework until I decide to procrastinate again.
7. Click `Stop`
8. Click `Upload`
9. Done


[downloads]: github.com/mishaturnbull/PySpeedTest/releases/latest
