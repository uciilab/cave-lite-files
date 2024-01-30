# Receive SPaT Messages and Manipulate Vehicle Motors
import J2735_201603_combined
import sys
import socket
import binascii
from gpiozero import DigitalOutputDevice, PWMOutputDevice
from math import pi
from time import sleep, time


def rpm():
    # rpm = int((pwmMot.value-0.083)/(1/240))
    rpm = int((pwmMot.value)/(1/240))
    print("Current RPM: ", rpm)
    return rpm

def angVel():
    w = rpm() * (2*pi/60)
    return w

def distToSig(timeEla):
    linSp = angVel() * wheelRad
    print("Current Speed: ", round(linSp,2))
    dist = round(linSp * timeEla, 2)
    return dist

# Motor Declarations
motorSTBY = DigitalOutputDevice(17)
motorA = DigitalOutputDevice(27)
motorB = DigitalOutputDevice(22)
pwmMot = PWMOutputDevice(18)    # pwm pin to control speed
motorSTBY.off()  # initialize motor driver
motorA.on()     # initialize motorA to on for forward direction
motorB.off()    # initialize motorB to off for forward direction
pwmMot.on()

# Initial Declarations
totDistance = int(sys.argv[1])/3.281    # received distance to signal in m
wheelRad = 0.1016 # 1/16   # radius of wheels in m og - 0.0365
#wheelCir = 2*pi*wheelRad    # wheel circumference in m
c1tDist = round(totDistance, 2)   # init dist to signal
timeEla = 0    #initiate time for dist travelled
counter = 0
distTravelled = 0
complete = 0

# listen to broadcast at declared IP + Port
ip_listen = "255.255.255.255" #"192.168.0.255" # "255.255.255.255"
port_listen = 5005
sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # declare receiving UDP connection
sk_listen.bind((ip_listen, port_listen))


msgIds=['0013'] # this can be updated to include other J2735 PSIDs
print("Total distance to signal (in meters): ", c1tDist)
sleep(4)
print("Vehicle listening.")
while(complete != 1):
    data = str(sk_listen.recvfrom(10000)[0])
    data = ''.join(data.split())
    # print(data)
    for id in msgIds:
        idx = data.find(id)
        # extract, decode, and use message from stream
        if(idx > -1 ):
            # extract
            if (int('0x'+data[idx+4],16)==8):
                lenstr=int('0x'+data[idx+5:idx+8],16)*2+6 
            else:
                lenstr=int('0x'+data[idx+4:idx+6],16)*2+6
            if(lenstr <= len(data)-idx+1):
                # decode
                msg = data[idx:idx+lenstr].encode('utf-8')
                decode = J2735_201603_combined.DSRC.MessageFrame
                decode.from_uper(binascii.unhexlify(msg))
                # decodedStr = str(decode())
                # print(decodedStr, '\n')

                moy = decode()['value'][1]['intersections'][0]['moy']
                timestamp = decode()['value'][1]['intersections'][0]['timeStamp']
                intersectionID = decode()['value'][1]['intersections'][0]['id']['id']
                intersectionName = decode()['value'][1]['intersections'][0]['name']
                instersectionPhaseArray = decode()['value'][1]['intersections'][0]['states']
                # print("Length instersectionPhaseArray: " + str(len(instersectionPhaseArray)))
                for phase in range(len(instersectionPhaseArray)):
                    currentPhase = decode()['value'][1]['intersections'][0]['states'][phase].get('signalGroup')
                    currentState = str(decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['eventState'])
                    minEndTime = decode()['value'][1]['intersections'][0]['states'][phase]['state-time-speed'][0]['timing']['minEndTime']
                    if (currentPhase == 2) :
                        phaseTwoState = currentState
                        # currentHour = ((moy/1440)-int(moy/1440))*24
                        # currentMinute = (currentHour-int(currentHour))*60
                        # count = currentMinute+(timestamp/100000)
                        timeEndTwo = minEndTime/600
                        print('Phase: ' + str(currentPhase))
                        print('  State: ' + currentState)
                    elif (currentPhase == 22) :
                        timeEndDouble = minEndTime/600
                countdown = (timeEndTwo-timeEndDouble)*100
                print("Time to next state: ", round(countdown,1))

                if (c1tDist > 0): 
                    if (phaseTwoState == "protected-Movement-Allowed") :
                        counter = time()
                        motorSTBY.on()
                        motorA.on()
                        #motorB.off()
                        pwmMot.value = 0.2
                        print('running in green')
                        
                    elif (phaseTwoState == "protected-clearance") :
                        counter = time()
                        motorSTBY.on()
                        motorA.on()
                        #motorB.on()
                        pwmMot.value = 0.05
                        print('running in yellow')
    
                    elif (phaseTwoState == "stop-And-Remain") :
                        counter = time()
                        motorSTBY.off()
                        motorA.off()
                        pwmMot.off()
                        print('stopped in red')
                        
                    else : 
                        counter = time()
                        motorSTBY.off()
                        motorA.off()
                        pwmMot.off()


                    # timeEla = time() - initTime # calculate time elapsed since init vehicle move
                    # print("Time since init movement: ", round(timeEla, 1))
                    if (counter == 0):
                        timeEla = timeEla
                    else:
                        timeEla = timeEla + (time() - counter)
                    print("Time elapsed: ", round(timeEla,2))
                    distTravelled = distTravelled + distToSig(timeEla)
                    print("Distance Travelled: ", round(distTravelled,2))
                    c1tDist = round(totDistance - distTravelled)
                    print("C1T distance to signal: ", round(c1tDist,2))
                    # print("PWM Value: ", pwmMot.value)
                    # print("PWM Freq: ", pwmMot.frequency)
                    # print("PWM status: ", pwmMot)
                    # print("mtrA Status: ", motorA)
                    # print("motorSTBY Status: ", motorSTBY)

                else:
                    pwmMot.off()
                    motorA.off()
                    motorSTBY.off()
                    #pwmMot.value = 0
                    complete = 1
                    print("Destination arrived, press Ctrl + C to end program")
                break
