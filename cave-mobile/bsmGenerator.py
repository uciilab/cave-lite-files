# BSM Generator
import J2735_201603_combined
import datetime
import ast
from time import sleep
from binascii import hexlify
from test import getLinSpeed

def getMsgCount(msgCount):
    msgCount += 1
    if (msgCount == 128):
        msgCount = 0
    return msgCount

def getSecMark():
    time = str(datetime.datetime.now())
    time = float(time.split(':')[2])
    secMark = int(time*1000)
    return secMark

def getSpeed():
    speed = int(getLinSpeed()*20)
    return speed

def encode():
    # encode the bsm
    msgFrame = J2735_201603_combined.DSRC.MessageFrame
    msgFrame.set_val(bsmDict)
    msgFrameUper = msgFrame.to_uper()
    encodedBSM = hexlify(msgFrameUper)
    return encodedBSM

count = 0

# read contents of bsmFrame.txt file
fout = open("bsmFrame.txt", 'r')
bsm = fout.readline()
fout.close()

# convert file contents to dict
bsmDict = ast.literal_eval(bsm)

# continually update values in dict and encode
while(1):
    count = getMsgCount(count)
    bsmDict['value'][1]['coreData']['msgCnt']  = count
    bsmDict['value'][1]['coreData']['secMark'] = getSecMark()
    bsmDict['value'][1]['coreData']['speed']   = getSpeed()

    encode()
    sleep(0.1) # generates a new BSM every 0.1 seconds, per SAE J2735