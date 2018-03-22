[Back to main page](index.html)

# Table of contents
1. [Basic Usage](#basic-usage)  
    1.1 [Running Speed Tests](#running-speed-tests)  
    1.2 [Uploading Results](#uploading-results)  
    1.3 [The ResNet Button](#the-resnet-button)  
    1.4 [Create Analysis File Button](#create-analysis-file-button)  
    1.5 [Example Usage](#example-usage)  
2. [What do the Numbers Mean?](#what-do-the-numbers-mean)  
    2.1 [Why Are There Two Rows?](#why-are-there-two-rows)  
    2.2 [What Are The Numbers?](#what-are-the-numbers)  
    2.3 [What Are "Good" Speeds?](#what-are-good-speeds)  

# Basic Usage
<div style="text-align:center">
    <img src ="https://github.com/mishaturnbull/PySpeedTest/raw/master/docs/window.png" />
</div>

## Running Speed Tests

In order to run speed tests, first, run the program as [described here](running), and the little window should pop up.  To start recording the internet speed (which you want to do), click the button that says "Start".

Before you do this, however, enter in the Location field where you are.  This *really* helps me sort through the data and make it useful -- I can't very well tell ResNet that the network speeds are slow in "McVey", but I can tell them it's slow in "McVey 3rd north".  This is surprisingly important.

When you no longer want to run speed tests, click the button that says "Stop".

## Uploading results

***PLEASE PLEASE PLEASE***, when you're done, click the upload button.  That button sends the data you recorded to my computer, which stores it for future analysis.  I can't do anything if I don't get the data you've been collecting.

After the results have been uploaded, they are cleared from your computer.  The main reason for this is to prevent duplicate data -- if, every time you upload data, you upload the same data + a bit more, I will rapidly accumulate vast amounts of identical data that becomes very difficult to filter out.  

## The ResNet Button

Pressing the ResNet button brings you to ResNet's support ticket page.  The sole purpose of this button is because I can never find this page and frequently want to submit tickets when the internet isn't working.  **Please don't flood ResNet with tickets for slow internet** -- they know about this -- but if it goes down, then let them know.

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
[running]: gettingstarted.html#running

# What Do The Numbers Mean?

The values displayed are the actual speeds resulting from the most recent, and overall average of all current internet tests.  They typically look something like this:

> Last: 15.63ms / 13.61Mbps↑ / 10.25Mbps↓  
> Avg: 18.29ms / 11.18Mbps↑ / 12.21Mbps↓  

## Why are There Two Rows?

The "Last:" row: displays the most recent speed test.  
The "Avg:" row: displays a running average of all tests made *this session*.  This resets every time you close the application.

## What are the numbers?

The rows are both formatted as follows:

> Last: Ping time / Upload speed↑ / Download speed↓  

Ping time: The duration it takes for your computer to establish a connection with the outside world.  Typically measured in milliseconds.  Lower is better, unlike the speeds.

Upload speed: The rate at which data is being sent from your computer to the outside world (uploading).  Typically measured in megabits per second.  Think of it as the speed that you can upload a documet to BlackBoard at.

Download speed: The rate at which data is being sent from the outside world to your computer.  Typically measured in megabits per second.  Think of it as the speed that you can download a game at.  This is the most common measure of speed and frequently the most important, since people tend to download a lot more than they upload (watching YouTube, Netflix, etc. as opposed to uploading an essay).

### Units used:

For ping times: milliseconds (ms)

For network speeds: measured in SI-prefixed bits per second rates:

  - Gbps: gigabit per second.  This is rare and extremely fast.
  - Mbps: megabit per second.  Most common.
  - Kbps: kilobit per second.  Pretty bad.
  - bps: Bit per second.  Probably faster to send your Facebook messages via snailmail.

## What are "Good" Speeds?

Well, that depends who you ask.

For reference, the FCC [defines broadband internet][fcc-broadband] as 3Mbps upload, and 25Mbps download.  [Speedtest.net][speedtest-fixed] cites the United States average speed as being 64.17Mbps download and 22.79Mbps upload.  Further, they cite US Internet as the fastest ISP in Minneapolis, offering download speeds of 65.51Mbps.  

So how much is "fast"?  Again, that depends on who you ask, what you're doing, and how impatient you are.  To put these speeds in context, the typical 5-page essay in Microsoft Word is approximately 35 kilobytes.  At a speed of 3 megabits per second upload, this could be sent to a server in 0.0116 seconds.  If you were to download the same document at a speed of 25 megabits per second, it would take 0.0014 seconds.  However, Word documents are just text (with some special bits).  Other items, such as images, are frequently much larger.  Higher-resolution, large images can be upwards of 6 or 7 megabytes, taking 2.08 seconds to download.  

All that assumes that you're the only person on the internet, sending and receving data with perfect transmission rates and the speed never differs from what it is set to.  In reality, I live in a dorm with ~300 other people who are also using the internet, and don't have a perfect transmission rate.

So, depending on what you're doing, the common accepted "fast" speeds might look something like:

|        Activity        | Best upload | Best download | Best ping |
| ---------------------- | ----------- | ------------- | --------- |
| Homework (Google Docs) |  >= 5 Mpbs  |   >= 5 Mpbs   | <= 20 ms  |
| Streaming video        |  >= 1 Mpbs  | >= 10-20 Mbps | <= 15 ms  |
| Online gaming          |  >= 15 Mbps |  >= 25 Mbps   | <= 12 ms  |

[fcc-broadband]: https://apps.fcc.gov/edocs_public/attachmatch/FCC-15-10A1_Rcd.pdf
[speedtest-fixed]: http://www.speedtest.net/reports/united-states/#fixed
