# Send NTCIP 1202 using UDP
import socket
import signal, sys
from binascii import unhexlify
from time import sleep

def signal_handler(sig, frame):
    print('\nExiting')
    sys.exit(0)  

# send payload to IP + port
ip = '127.0.0.1' #input('Enter IP Address to send to: ')
port = '6053' #input('Enter Port to send to: ')
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# open and read from file, then close file
f = open('fixedFull.txt', 'r') # change to pcapOutput.txt for initial TSC pcap extraction
Lines = f.readlines()
f.close()

print('Sending.\nPress Ctrl+C to exit')
sleep(2)
while(1):
    for line in Lines:
        data = line.strip('\n')
        # print(data)                        # uncomment to view stream 
        # send Hex string to port
        unhexed = unhexlify(data)
        sk.sendto(unhexed,(ip,int(port)))
        sleep(0.1)                          # 0.1 for NTCIP 1202

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
