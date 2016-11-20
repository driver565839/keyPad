# Servo Control
import time
import wiringpi
import RPi.GPIO
import random
import time
import requests
import numpy
import os
from twilio.rest import TwilioRestClient
from matrix_keypad import RPi_GPIO
########################################################################3
#Function Junction

os.chdir('/home/pi/gabe/keypad/')

def timeout():
    print("TIMED OUT OH NO")
    
    
    
def openDoor():
    wiringpi.pwmWrite(18, 150)  #Open the door
    RPi.GPIO.output(20,True)
    RPi.GPIO.output(17,False)
    print("OPEN DOOR")
    time.sleep(5)
    print("CLOSE DOOR")
    wiringpi.pwmWrite(18, 90)  #Close the door
    RPi.GPIO.output(20,False)
    RPi.GPIO.output(17,True)

    
def badPin():
    print("Phase two bad")
    
    
def badVerify():
    print("VERY BAD")
    
def badEither():
    RPi.GPIO.output(20,False)
    for i in range(5):
        RPi.GPIO.output(17,False)
        time.sleep(.15)
        RPi.GPIO.output(17,True)
        time.sleep(.3)
    RPi.GPIO.output(17,True)
    
    
def readcode():
    #Reads in numbers until the pound is pressed. Star resets
    attempt = ''
    i = 0
    exit = 0
    brk = 0
    start = time.time()  #Start the timer
    timeout = 30
    while True:  #Loop until pound sign or 60 seconds
        #return '1869'
        key = kp.getKey()
        
        while (key) == None:
            key = kp.getKey()
            end = time.time()  #End the timer
            if(end-start > timeout):  #Timeout if more than a minute elapses
                brk = 1
                break
                
        if(brk == 1):
            break
            
        #key = kp.getKey()
        #Get the key pressed
        print("Key pressed:", key,attempt)
        key = str(key)
        if key == '*':  #Reset
            exit +=1
            if(exit >= 2):
                return 'exit'
            attempt = ''
            start = time.time()
        elif key == '#':  #Return the final number
            print("attempt:",attempt)
            while kp.getKey() != None: #Wait until the key is released
                pass
            return attempt
        else:
            exit = 0
            attempt += key  #Add the key press to the code

        

        while kp.getKey() != None: #Wait until the key is released
            end = time.time()  #End the timer
            if(end-start > timeout):  #Timeout if more than a minute elapses
                brk = 1
                break
        if(brk == 1):
            break
    
    return 'timeout'
##########################################################################################
#Initialize all the things:

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)


RPi.GPIO.setmode (RPi.GPIO.BCM)

RPi.GPIO.setup(17, RPi.GPIO.OUT)
RPi.GPIO.setup(20, RPi.GPIO.OUT)
wiringpi.pwmWrite(18, 90)  #Close the door
account_sid = "ACbdbc6719e395ca314cafbb74a38f9441"
auth_token = "75e5b8e3f4b7c5e56d2937eed007116a"
client = TwilioRestClient(account_sid, auth_token)

lst=[]
temp = []
with open('settings.txt') as f:
    a = f.readlines()
    for line in a:
        lst.append(line.strip().split(','))


kp = RPi_GPIO.keypad(columnCount = 4)
attempt = '0000'
##########################################################################################
#MAIN LOOP:
RPi.GPIO.output(17,True)
while True:
    print("Phase One")
    attempt = readcode()  #Run the function to read in the keys
    good = 0
    #print("attempt: ", attempt)
    for i in range(len(lst)):  #Loop through to see if the passcode matches anyones
        if(attempt == lst[i][1]):
            good = 1
            break
    #print("Good?: ",good)
    if(attempt == 'exit'):
        continue
    if(attempt == 'timeout'):
        timeout()
        continue
    while kp.getKey() != None: #Wait until the key is released
        pass
    if good == 1:  #If the code is good
        print("Phase two good")
        #Do the second check.
        #Text code in
        newcode =  str(int(9999*random.random()))     
        print("newcode",newcode)
        message = client.messages.create(to=lst[i][0], from_="+14128524518",body=newcode)
        #print("HERE2")
        attempt = readcode()
        #checkKeypad = '*'
        if attempt == newcode:  #If the code is good
            openDoor()
        else:
            badVerify()
            badEither()
    
    else:
        badPin()
        readcode()
        badEither()
    
RPi.GPIO.output(17,False)
RPi.GPIO.cleanup()  #This needs to be run last
