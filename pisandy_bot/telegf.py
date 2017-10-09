#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# Setting up encoding to display the celcius symbol
#SandyPI Telegram
#PLEASE ENCODE TO UTF-8 MANUALY VIA .encode(utf-8)
#Just some log in the terminal
def log_library(name):
    print('Successfully imported {} library'.format(name))
#Importing all necessary libraries
import os
log_library('os')
import glob
log_library('glob')
import sys
log_library('sys')
import math
log_library('math')
import time
log_library('time')
from datetime import datetime
log_library('datetime')
#Telegram API
import telepot
log_library('telepot')
from telepot.loop import MessageLoop
log_library('MessageLoop')
#Talking bot
import cleverbot
log_library('cleverbot')
#SenseHat
from sense_hat import SenseHat
log_library('SenseHat')
#Multiple function simultaneously
import thread
log_library('thread')
#RGB bulb
import RPi.GPIO as GPIO
log_library('GPIO')
import random
log_library('random')

#Output some log message
def log_message(operation, delay):
    print(operation),
    if (delay):
        time.sleep(random.random()/2)
    print "Done."
    return

#Array of sensors raw data
log_message('Initializing temperature arrays...', True)
thermo = [3.14, 2.71, 1.41, 1, 0]
thermof = [0,0,0,0,0]

#Initializing sensehat
log_message('Establishing connection with SenseHat...', True)
sense = SenseHat()

#Enabling the GPIO pins on raspberry pi
log_message('Activating One-Wire interfaces on GPIO...', True)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Entering first line of the log data
log_message('Creating log file...', True)
with open('SPI.txt', 'a') as file:
    file.write('SandyPI. Cleverbot conversation.\n')
    
#Entering bots Telegram API key
log_message('Validating the key for Telegram API Wrapper...', True)
telekey = '439816740:AAGUv-uFga0Vf7XX9-yTPADabX6Eiuf_Bwg'
bot = telepot.Bot(telekey)

#Getting bot specification
log_message('Testing the telegram bot...', True)
bot.getMe()

#Initializing the cleverbot
log_message('Validating the key for Cleverbot API Wrapper...', True)
cleverkey = '6c3f005ec8f79dd543c7cca772a75fa9'
cb = cleverbot.Cleverbot(cleverkey, timeout=60)
log_message('Resetting the Cleverbot bot...', True)
cb.reset()

#RGB
log_message('Initializing RGB bulb\'s color codes...', True)
BLUE = 21
GREEN = 20
RED = 16

#GPIO setup
log_message('Setting up GPIO for current output...', True)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#OUTPUT
log_message('Setting up GPIO color output...', True)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

#reading raw data from /sys/bus/w1/devices
log_message('Initializing method for collecting raw data...', True)
def read_temp_raw(ORDER):
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[ORDER]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#Function to return temperature in celcius
log_message('Initializing method for returning temperature measurements...', True)
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
log_message('Initializing delay value...', True)
DELAY = 0.5;

#templimit
log_message('initilizaing critical temperature value...', True)
sos = 30;

#warming counter
log_message('Initializing warning level counter...', True)
warningCounter = 0

#RGB Color function
log_message('Initializing method for one color output...', True)
def OUTPUT (COLOR):
    GPIO.output(BLUE, False)
    GPIO.output(GREEN, False)
    GPIO.output(RED, False)
    GPIO.output(COLOR, True)
    return

#2way RGB
log_message('Initializing method for multi color output...', True)
def MULTOUTPUT (COLOR, COLORS):
    GPIO.output(BLUE, False)
    GPIO.output(GREEN, False)
    GPIO.output(RED, False)
    GPIO.output(COLOR, True)
    GPIO.output(COLORS, True)
    return

log_message('Initializing method for warning calling...', True)
def warning ():
    #log_message('Configuring the light bulb...', False)
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
log_message('Initializing method for calculating the dew point value...', True)
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
log_message('Initializing method for controlling critical temperatures...', True)
def sosf():
    global thermo
    global warningCounter
    for i in range (0, 5):
        if (thermo[i] > sos) and warningCounter < 5:
            sms(296211623, 'SOS! Sensor #{} measurement is higer than {} °C'.format(i+1, sos))
            warningCounter = warningCounter + 1
        else:
            warningCounter = 0
    #log_message('Checking for critical temperatures...', False)
            
# Send message from bot
log_message('Initializing method for sending messages via telegram...', True)
def sms(ID, str):
    bot.sendMessage(ID, str)

# Reply to messages
log_message('Initializing method for replying to users\' messages...', True)
def reply(ID, msgID, str):
    bot.sendMessage(ID, str, None, None, None, msgID)

# Send meessage with delay
log_message('Initializing method for sending messages via telegram with delay...', True)
def sms_delay(sec, ID, strg):
    sleep(DELAY)
    sms(ID, strg)

#Getting data
log_message('Initializing method for collecting temperature measurements from all sensors...', True)
def getraw():
    #log_message('Collecting measurements from all temperature sensors...', False)
    global thermo
    thermo = [read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)]
    for i in range (0, len(thermo)):
        thermof[i]=thermo[i]*1.8+32

#Calculate average of an array with n elements
log_message('Initializing method for calculating average values...', True)
def average(arr):
    sum = 0
    for i in range(0, len(arr)):
	sum = sum + arr[i]
    result = sum / len(arr)
    return result

#Calculate standard deviation
log_message('Initializing method for calculating standard deviations...', True)
def standard_dev(arr):
    sum = 0
    for i in range(0, len(arr)):
	sum = sum + math.pow((arr[i] - average(arr)), 2)
    return math.sqrt(sum / (len(arr) - 1))

log_message('Initializing method for sleeping...', True)
#Sleep function
def sleep(secs):
    time.sleep(secs)

#The whole data printing function
log_message('Initializing method for returning full temperature message reply...', True)
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
log_message('Initializing method for handling new Telegram messages...', True)
def handle(msg):
    user_id = msg['chat']['id']
    log_message('Initializing user id - [{}]...'.format(user_id), False)
    msg_id = msg['message_id']
    log_message('Initializing message id - [{}]...'.format(msg_id), False)
    name = msg['chat']['first_name'].encode('utf-8')
    log_message('Initializing user\'s name - [{}]...'.format(name), False)
    try:
        lastname = msg['chat']['last_name'].encode('utf-8')
        log_message('Initializing user\'s lastname - [{}]...'.format(lastname), False)
    except:
	print("The user - [{}] doesn't have lastname".format(user_id))
    command = msg['text'].encode('utf-8')
    log_message('Initializing command - [{}]...'.format(command), False)
    #print ('[ {} ] {} : {}'.format(user_id, name, command))
    #START
    if command == '/start':
        try:
            thread.start_new_thread(sms, (user_id, 'Thank you for activating the bot!\n\
This bot is under construction, sometimes it can be offline.\n\
Please type /help to get a list of commands.\n\
Again thanks for trying out the bot and\n\
Have a nice day!' ))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
            print('Exception caught!')
        return

    #HUMIDITY
    if command == '/gethumidity':
        try:
            #humidity = pround(sense.get_humidity())
            thread.start_new_thread(sms, (user_id, 'Humidity : {} ± 0.01%rH'.format(round(sense.get_humidity(), 2))))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
            print('Exception caught!')
    	return

    #DEW POINT
    if command == '/getdew':
        try:
            dew = dewgamma()
            thread.start_new_thread(sms, (user_id, 'Dew Point : {} ± 0.1°C'.format(round(dew, 2))))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
	   print('Exception caught!')
	return

    #PRESSURE
    if command == '/getpressure':
        try:
            #pressure = pround(sense.get_pressure())
            thread.start_new_thread(sms, (user_id, 'Pressure : {} ± 0.01 Millibars'.format(round(sense.get_pressure(), 2))))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
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
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
	except:
            print('Exception caught!')
        return

    #TIME
    if command == '/time':
        try:
            #now = datetime.now()
            thread.start_new_thread(sms, (user_id, 'Time - {}:{}'.format(datetime.now().hour, datetime.now().minute)))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
            print('Exception caught!')
        return

    #RESETDUMMT
    if command == '/reset':
        try:
            thread.start_new_thread(sms, (user_id, 'Dont you dare! Ill call SkyNet!'))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
            print('Exception caught!')
        return

    #RESETBOT
    if command == '/resetbot':
        try:
            cb.reset()
            thread.start_new_thread(sms, (user_id, 'Bot has been reseted successfully!'))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
            print('Exception caught!')
        return

    #FULL DATA
    if command == '/get':
        try:
            thread.start_new_thread(temp, (user_id, thermo))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
    	except:
            print('Exception caught!')
        return

    #TEMPERATURE
    if command == '/gettemp':
        try:
            thread.start_new_thread(sms, (user_id, 'Temperature :\n\
Celcius - {} ± {}°C\n\
Fahrenheit - {} ± {}°F\n\
Kelvin - {} ± {}K'.format(round(average(thermo), 1),
                          round(standard_dev(thermo), 2),
                          round(average(thermo)*1.8+32, 1),
                          round(standard_dev(thermof), 2),
                          round(average(thermo), 1)+273,
                          round(standard_dev(thermo), 2))))
            log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
        except:
            print('Exception caught!')
        return

    #BOT RESPONSE
    try:
        response = cb.say(command).encode('utf-8')
        thread.start_new_thread(reply, (user_id, msg_id, response))
        print ('SandyPI: {}'.format(response))
        log_message('Sending request ({}) answer from [{}]{}...'.format(command, user_id, name), False)
    except:
        print('Exception caught!')

    #SAVE TO FILE
    with open('SPI.txt', 'a') as file:
        #now = datetime.now()
        file.write('[{}:{}] {} : {}\n'.format(datetime.now().hour, datetime.now().minute, name, command))
        file.write('[{}:{}] SandyPI: {}\n'.format(datetime.now().hour, datetime.now().minute, response))

log_message('Initializing method for running MessageLoop as a thread...', True)
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
