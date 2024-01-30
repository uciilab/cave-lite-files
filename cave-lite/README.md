## Overview
CAVe-Lite is the smaller version of CAVe-in-a-Box. CAVe-Lite is meant to be used in a classroom setting to teach and demonstrate
the network connections and message flow for SAE J2735 messages. This script will allow for a SPaT (Signal Phase and Timing) message to 
be translated from a pre-recorded Traffic Signal Controller (NTCIP 1202) message. The SPaT Message is broadcast to the network the 
Raspberry Pi is connected to. A traffic light and CARMA 1-Tenth or CAVe-Mobile vehicle are used to demonstrate how SAE J2735 Messages can be used. 

Instructions for downloading and using CAVe-Mobile can be found in the cave-mobile repository.

The attached NTCIP 1202 cycle contains the following signal phases:
Green state = 15 seconds
Yellow state = 3 seconds
Red state = Green + Yellow + 2 second all phases red (20 seconds)

## Prerequisites:
* V2X Hub (arm64, latest) https://github.com/usdot-fhwa-OPS/V2X-Hub; https://usdot-carma.atlassian.net/wiki/spaces/V2XH/pages/1886158849/V2X-Hub+Docker+Deployment
* python3  `sudo apt install python3`
* pip3     `sudo apt install python3-pip`
* tkinter  `sudo apt install python3-tk`
* pycrate  `pip3 install pycrate`
* gpiozero `pip3 install gpiozero`

## Usage
CAVe-Lite Raspberry Pi default Static IP set to: 192.168.0.146

1. Run:
	```
	$ cd ~/cave-lite/
	$ ./rc.local start
	```

2. To stop:
	```
	$ ./rc.local stop
	```