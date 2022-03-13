# Importing Libraries
import serial
import time
import struct

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

# dataToSend = Array (up to 5 elements corresponding to each finger)
def arduinoWrite(dataToSend):
    #arduino.write(struct.pack('BBBBBB',255,dataToSend[0],dataToSend[1],dataToSend[2],dataToSend[3],dataToSend[4]))
    arduino.write(bytes('255', 'utf-8'))
    time.sleep(0.05)
    for i in range(len(dataToSend)):
        arduino.write(bytes(str(dataToSend[i]), 'utf-8'))
        print(bytes(str(dataToSend[i]), 'utf-8'))
        time.sleep(0.05)
    #data = arduino.readline()
    #print(data)

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
    print(dataToSend)
    #print(True)
    return True 
    
while True:
    num1 = int(input("Enter a number: ")) # Taking input from user
    num2 = int(input("Enter a number: ")) # Taking input from user
    num3 = int(input("Enter a number: ")) # Taking input from user
    num4 = int(input("Enter a number: "))# Taking input from user
    num5 = int(input("Enter a number: ")) # Taking input from user

    transmit([num1,num2,num3,num4,num5])
    
