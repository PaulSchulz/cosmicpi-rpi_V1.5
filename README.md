# Cosmic Pi Software on the Raspberry Pi

This software runs on the raspberry pi, which is integral to the CosmicPi V1.5.
The central point is a SQLite database into which data is stored, as well as read from.
More instructions will follow when the software has reached the state of the V2 mock-up software.

## Current features
*   Create a SQLite database
*   Read the serial output from the Arduino Due, parse it and store the information into the SQLite database
*   Application for the UI, under development

## Needed features to match up with the Version 2 mock-up software
*   Read data from the detector into the SQLite database    [DONE]
*   Display basic information in the Web-UI                 [In development]
*   Start application on boot                               [Not yet started]
*   Start hotspot on boot                                   [Not yet started]
*   Connect to a different WiFi via the webinterface        [Not yet started]
*   Working install procedure                               [Not yet started]
*   SystemD services for all components                     [Not yet started]
    *   Detector readout
    *   WebUI
    *   Hotspot
    *   Database maintainance


## Installation
Clone this repository to the home folder of your CosmicPi (e.g. `/home/pi`)
then run:

```./install```

This will currently do nothing. Just clone the repository.

## Run
The software is normally controled via SystemD. This is not yet implemented, so you will need to run the scripts directly.


