# SAE J2735 Message Sender
import socket
import binascii as ba
from time import sleep
from bsmGenerator import encode # uncomment to use generated BSMs


ip_send = '192.168.0.255'
broadcast = '255.255.255.255'
port_send = 26789

# uncomment block to continually send single, non-generated BSM
# read contents of 'bsm.txt' file
#f = open('bsm.txt', 'r')
#Lines = f.readlines()
#f.close()

print("Broadcasting messages.")
while (1):
    # uncomment block to send generated BSMs
    data = str(encode)
    data = data.strip('\n') # removes any new line characters
    # print(data) # uncomment to view stream
    # send Hex string to port
    unhexed = ba.unhexlify(data)
    sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk_send.bind((ip_send, 0))
    sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
    sk_send.sendto(unhexed, (broadcast, port_send)) # broadcast message
    sk_send.close()
    sleep(0.1) # 0.1 to send 10 BSMs/second, per SAE J2735

    # uncomment block to send single, non-generated BSM
    #for line in Lines:
    #    data = line.strip('\n') # removes any new line characters
    #    # print(data) # uncomment to view stream
    #    # send Hex string to port
    #    unhexed = ba.unhexlify(data)
    #    sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    sk_send.bind((ip_send, 0))
    #    sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
    #    sk_send.sendto(unhexed, (broadcast, port_send)) # broadcast message
    #    sk_send.close()
    #    sleep(0.1) # 0.1 to send 10 BSMs/second, per SAE J2735
