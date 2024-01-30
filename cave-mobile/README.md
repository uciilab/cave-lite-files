This mobile.sh script will listen to broadcasts in the network it is connected to and broadcast to the same network.
It is specifically looking for SAE J2735 SPaT messages. Once SPaT is retreived, the message is decoded and phase information 
is extracted. This phase state and timing information is used to control the motor of a CARMA 1-Tenth vehicle. 

Prerequisites: 
python3  # sudo apt install python3
pip3     # sudo apt install python3-pip3
pycrate  # pip3 install pycrate
gpiozero # pip3 install gpiozero

Mobile Kit Raspberry Pi default Static IP set to: 192.168.0.110

1. Run mobile kit:
	cd ~/cave-mobile
	bash mobile.sh
	
2. To stop script: <Ctrl-C>