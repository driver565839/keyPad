# Servo Control
import time
import wiringpi
import RPi.GPIO
import random
import time
import requests
import numpy
from twilio.rest import TwilioRestClient
from matrix_keypad import RPi_GPIO


def readcode():
    #Reads in numbers until the pound is pressed. Star resets
    attempt = ''
    i = 0
    start = time.time()#Start the timer
    while True:#Loop until pound sign or 60 seconds
        #return '1869'
        key = kp.getKey()
        while (key) == None:
            key = kp.getKey()
        #key = kp.getKey()
        #Get the key pressed
        print("Key pressed:", key,attempt)
        key = str(key)
        if key == '*':  #Reset
            attempt = ''
        elif key == '#':  #Return the final number
            return attempt
        else:
            attempt += key  #Add the key press to the code

        end = time.time()  #End the timer
        if(end-start > 5):  #Timeout if more than a minute elapses
            break

        while kp.getKey() != None: #Wait until the key is released
            a=0
    return 'Error: Timeout'

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

RPi.GPIO.setup(2, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
wiringpi.pwmWrite(18, 90)#Close the door
account_sid = "ACbdbc6719e395ca314cafbb74a38f9441"
auth_token = "75e5b8e3f4b7c5e56d2937eed007116a"
client = TwilioRestClient(account_sid, auth_token)

lst=[]
temp = []
with open('settings.txt') as f:
    a = f.readlines()
    for line in a:
        lst.append(line.strip().split(','))


url = 'https://api.twilio.com/2010-04-01/Accounts/AC123456abc/Messages'
kp = RPi_GPIO.keypad(columnCount = 4)
attempt = '0000'
iiii = 0
while iiii==0:
    iiii+=1
    checkpad = kp.getKey()
    while (checkpad) == None:
        checkpad = kp.getKey()
    #print(checkKeypad)
    if checkKeypad == '*':#If its the start key
        print("Star Pressed")
        attempt = readcode()#Run the function to read in the keys
    good = 0
    print("attempt: ", attempt)
    for i in range(len(lst)):#Loop through to see if the passcode matches anyones
        if(attempt == lst[i][1]):
            good = 1
            break
    #print("Good?: ",good)
    if good == 1:#If the code is good
        #Do the second check.
        #Text code in
        newcode =  str(int(9999*random.random()))     
        print("newcode",newcode)
        print("HERE")
        message = client.messages.create(to=lst[i][0], from_="+14128524518",body=newcode)
        print("HERE2")
        checkKeypad = kp.getKey()#Read in the keyvalue
        #checkKeypad = '*'
        if checkKeypad == "*":#If its the start key
            #print("SECOND STAR")
            attempt = readcode()#Run the function to read in the keys
        if attempt == newcode:#If the code is good
            wiringpi.pwmWrite(18, 150)#Open the door
            #print("OPEN DOOR")
            time.sleep(5)
            #print("CLOSE DOOR")
            wiringpi.pwmWrite(18, 90)#Close the door


    

RPi.GPIO.cleanup()#THis needs to be run last
