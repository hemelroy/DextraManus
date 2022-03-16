# Written by:  Rishihesan Kuhesan
#              Asimov Automation, Group 23
# Written for: Dextramanus Capstone Project
#             
# Dependencies: pip install pyserial
#
# NOTE SERIAL COMM TRANSMIT FUNCTION
# 
# Sample code:
#
# while (True):
#     isWorking = transmit(dataToSend)
#     if not isWorking:
#         break
#     time.sleep(1)
# 
# Input: dataToSend is a 5-dimensional array with 0-180 integer for each finger except   
#         0-150 integer for the thumb indicating how many degrees each servo should spin. 
#         The order is: [Thumb (0-150 Int), Index (0-180 Int), Middle (0-180 Int), 
#                       Ring (0-180 Int), Pinky (0-180 Int)]
#
# Output: Returns true or false if it is working. True means all good. False means
#         unexpected input (which should emergency stop imo)
#
#
# Note : time.sleep works at minimal with 1 second for full range of motion between 0-180
#         degrees for the servos. For smaller range of motion, you can try 0.75 seconds.    
#       

import serial
import serial.tools.list_ports
import time
from datetime import datetime

COM_PORT = None
arduino = None

#Returns serial port of an arduino device if connected to machine
def getSerialPort():
    global COM_PORT

    arduino_port = None
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p.description:
            arduino_port = p[0]
            if COM_PORT != arduino_port:
                COM_PORT = str(arduino_port)
                establishConnection()

    return arduino_port

def establishConnection():
    global arduino
    arduino = serial.Serial(port=COM_PORT, baudrate=115200)

# dataToSend = Array (up to 5 elements corresponding to each finger)
def arduinoWrite(dataToSend):
    # arduino.write(bytes('<','utf-8'))
    # #time.sleep(0.03)
    # arduino.write(bytes('255', 'utf-8'))
    # #time.sleep(0.03)
    # for i in range(len(dataToSend)):
    #     arduino.write(bytes(',', 'utf-8'))
    #     #time.sleep(0.03)
    #     arduino.write(bytes(str(dataToSend[i]), 'utf-8'))
    #     #time.sleep(0.03)
    # arduino.write(bytes('>','utf-8'))
    # #time.sleep(0.03)
    # #data = arduino.readline()
    # #print(data)
    arduino.write(bytes(('<255,' + str(dataToSend[0]) + ',' + str(dataToSend[1]) + ',' + str(dataToSend[2]) + ',' + str(dataToSend[3]) + ',' + str(dataToSend[4]) + '>'), 'utf-8'))

# dataToSend = Array (up to 5 elements corresponding to each finger)
# returns True if successul, False if fail
def transmit(dataToSend):
    if len(dataToSend) != 5:
        #print(False)
        return False
        
    for i in range(len(dataToSend)):
        if isinstance(dataToSend[i], (int, float)):
            dataToSend[i] = int(dataToSend[i])
            if dataToSend[i] < 0 or dataToSend[i] > 180:
                #print(False)
                return False
        else:
            #print(False)
            return False

    arduinoWrite(dataToSend)
    print(datetime.now())
    #print(dataToSend)
    #print(True)
    return True