#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Setting up encoding to display the celcius symbol
#SandyPI Telegram
#PLEASE ENCODE TO UTF-8 MANUALY VIA .encode(utf-8)
import os
import glob
import sys
import math
#Delays
import time
from datetime import datetime
#Telegram API
import telepot
from telepot.loop import MessageLoop
#Talking bot
import cleverbot
#SenseHat
from sense_hat import SenseHat
#Multiple function simultaneously
import thread
#RGB bulb
import RPi.GPIO as GPIO

#Array of sensors raw  data
thermo = [3.14, 2.71, 1.41, 1, 0]

#Initializing sensehat
sense = SenseHat()

#Enabling the GPIO pins on raspberry pi
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Entering first line of the log data
with open('SPI.txt', 'a') as file:
    file.write('SandyPI. Cleverbot conversation.\n')

#Entering bots Telegram API key
telekey = ''
bot = telepot.Bot(telekey)

#Getting bot specification
bot.getMe()

#Initializing the cleverbot
cleverkey = ''
cb = cleverbot.Cleverbot(cleverkey, timeout=60)
cb.reset()

#RGB
BLUE = 21
GREEN = 20
RED = 16

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#OUTPUT
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

#reading raw data from /sys/bus/w1/devices
def read_temp_raw(ORDER):
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[ORDER]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Function to return temperature in celcius
def read_temp(NUMBER):
    lines = read_temp_raw(NUMBER)
    while lines[0].strip()[-3:] != 'YES':
        #time.sleep(0.2)
        lines = read_temp_raw(NUMBER)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#Just Delay
DELAY = 0.5;

#templimit
sos = 30;

#warming counter
warningCounter = 0

#RGB Color function
def OUTPUT (COLOR):
    GPIO.output(BLUE, False)
    GPIO.output(GREEN, False)
    GPIO.output(RED, False)
    GPIO.output(COLOR, True)
    return

#2way RGB
def MULTOUTPUT (COLOR, COLORS):
    GPIO.output(BLUE, False)
    GPIO.output(GREEN, False)
    GPIO.output(RED, False)
    GPIO.output(COLOR, True)
    GPIO.output(COLORS, True)
    return

def warning ():
    averround = round(average(thermo), 2)
    if averround < 30:
	if averround > 26:
            MULTOUTPUT(RED, GREEN)
	    return
        OUTPUT(GREEN)
	return
    OUTPUT(RED)
    return

#DEW POINT
def dewgamma():
    b = 18.678
    c = 257.14
    RH = sense.get_humidity()
    global thermo
    #Below goes just the dew point formula with +-0.1C uncertainty
    T = (thermo[0]+thermo[1]+thermo[2]+thermo[3]+thermo[4])/5
    g = math.log(RH / 100) + ( (b * T) / (c + T) )
    result = (c * g) / (b - g)
    return result

#SOS function
def sosf():
    global thermo
    global warningCounter
    for i in range (0, 5):
        if (thermo[i] > sos) and warningCounter < 5:
            sms(296211623, 'SOS! Sensor #{} measurement is higer than {} °C'.format(i+1, sos))
            warningCounter = warningCounter + 1
        else:
            warningCounter = 0

# Send message from bot
def sms(ID, str):
    bot.sendMessage(ID, str)

def reply(ID, msgID, str):
    bot.sendMessage(ID, str, None, None, None, msgID)

# Send meessage with delay
def sms_delay(sec, ID, strg):
    sleep(DELAY)
    sms(ID, strg)

#Getting data
def getraw():
    global thermo
    thermo = [read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)]

#Calculate average of an array with n elements
def average(arr):
    sum = 0
    for i in range(0, len(arr)):
	sum = sum + arr[i]
    result = sum / len(arr)
    return result

#Calculate standard deviation
def standard_dev(arr):
    sum = 0
    for i in range(0, len(arr)):
	sum = sum + math.pow((arr[i] - average(arr)), 2)
    return math.sqrt(sum / (len(arr) - 1))

#Sleep function
def sleep(secs):
    time.sleep(secs)

#The whole data printing function
def temp(ID, thermo):
    humidity = round(sense.get_humidity(), 2)
    pressure = round(sense.get_pressure(), 2)

    sms_delay(1, ID, 'Connecting to host...')
    sms_delay(1, ID, 'Sending request...')
    sms_delay(1, ID, 'Receiving some weird numbers...')
    sms_delay(1, ID, 'Trying to resolve...')
    sms_delay(1, ID, 'Uploading results...')

    sms(ID, 'Measurements from temperature sensors\n\
First :      {} °C\n\
Second : {} °C\n\
Third :     {} °C\n\
Fourth :  {} °C\n\
Fifth :      {} °C\n\
\n\
Humidity : {} %rH\n\
Pressure : {} Millibars'.\
        format(thermo[0], thermo[1], thermo[2], thermo[3], thermo[4], humidity, pressure))
    sms(ID, 'This bot is showing temperature, humidity and pressure of air \n\
from my room using raspberry pi with Sense HAT\n\
and 5 DS18B20 temperature sensors')

#Handling the messages
def handle(msg):
    user_id = msg['chat']['id']
    msg_id = msg['message_id']
    #user_id = msg['from']['chat_id']
    name = msg['chat']['first_name'].encode('utf-8')
    try:
        lastname = msg['chat']['last_name'].encode('utf-8')
    except:
	print("The user - [{}] doesn't have lastname".format(user_id))
    command = msg['text'].encode('utf-8')
    print ('[ {} ] {} : {}'.format(user_id, name, command))
    #START
    if command == '/start':
        try:
            thread.start_new_thread(sms, (user_id, 'Thank you for activating the bot!\n\
This bot is under construction, sometimes it can be offline.\n\
Please type /help to get a list of commands.\n\
Again thanks for trying out the bot and\n\
Have a nice day!' ))
        except:
            print('Exception caught!')
        return

    #HUMIDITY
    if command == '/gethumidity':
        try:
            #humidity = pround(sense.get_humidity())
            thread.start_new_thread(sms, (user_id, 'Humidity : {} %rH'.format(round(sense.get_humidity(), 2))))
        except:
            print('Exception caught!')
    	return

    #DEW POINT
    if command == '/getdew':
        try:
            dew = dewgamma()
            thread.start_new_thread(sms, (user_id, 'Dew Point : {} °C'.format(round(dew, 2))))
        except:
	   print('Exception caught!')
	return

    #PRESSURE
    if command == '/getpressure':
        try:
            #pressure = pround(sense.get_pressure())
            thread.start_new_thread(sms, (user_id, 'Pressure : {} Millibars'.format(round(sense.get_pressure(), 2))))
        except:
            print('Exception caught!')
        return

    #HELP
    if command == '/help':
        try:
            thread.start_new_thread(sms ,(user_id, 'Command list\n\
/get to get data from all sensors\n\
/gettemp to get mean temperature\n\
/gethumidity to get humidity level\n\
/getpressure to get pressure level\n\
/getdew to get the dew point\n\
/help to get this help screen\n\
/time to get current time (local)\n'))
	except:
            print('Exception caught!')
        return

    #TIME
    if command == '/time':
        try:
            #now = datetime.now()
            thread.start_new_thread(sms, (user_id, 'Time - {}:{}'.format(datetime.now().hour, datetime.now().minute)))
        except:
            print('Exception caught!')
        return

    #RESETDUMMT
    if command == '/reset':
        try:
            thread.start_new_thread(sms, (user_id, 'Dont you dare! Ill call SkyNet!'))
        except:
            print('Exception caught!')
        return

    #RESETBOT
    if command == '/resetbot':
        try:
            cb.reset()
            thread.start_new_thread(sms, (user_id, 'Bot has been reseted successfully!'))
        except:
            print('Exception caught!')
        return

    #FULL DATA
    if command == '/get':
        try:
            thread.start_new_thread(temp, (user_id, thermo))
    	except:
            print('Exception caught!')
        return

    #TEMPERATURE
    if command == '/gettemp':
        try:
            thread.start_new_thread(sms, (user_id, 'Temperature :\n\
Celcius - {} °C\n\
Fahrenheit - {} °F\n\
Kelvin - {} K'.format(round(average(thermo), 1), round(average(thermo)*1.8+32, 1), round(average(thermo), 1)+273)))
        except:
            print('Exception caught!')
        return

    #BOT RESPONSE
    try:
        response = cb.say(command).encode('utf-8')
        thread.start_new_thread(reply, (user_id, msg_id, response))
        print ('SandyPI: {}'.format(response))
    except:
        print('Exception caught!')

    #SAVE TO FILE
    with open('SPI.txt', 'a') as file:
        #now = datetime.now()
        file.write('[{}:{}] {} : {}\n'.format(datetime.now().hour, datetime.now().minute, name, command))
        file.write('[{}:{}] SandyPI: {}\n'.format(datetime.now().hour, datetime.now().minute, response))

        
MessageLoop(bot, handle).run_as_thread()

while 1:
    thread.start_new_thread(getraw, ())
    thread.start_new_thread(sosf, ())
    thread.start_new_thread(warning, ())
    try:
        bot.getMe()
    except:
        print('EXCEPTION GETME')
    time.sleep(8)
