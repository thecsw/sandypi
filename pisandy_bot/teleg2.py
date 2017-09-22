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
from telepot.loop import OrderedWebhook
#Talking bot
import cleverbot
#SenseHat
from sense_hat import SenseHat
#Multiple function simultaneously
import threading
import thread

#Initializing sensehat
sense = SenseHat()

#Enabling the GPIO pins on raspberry pi
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#Entering first line of the log data
with open('SPI.txt', 'a') as file:
    file.write('SandyPI. Cleverbot conversation.\n')
  
#Entering bots Telegram API key
telekey = 'TELEGRAM BOT API'
bot = telepot.Bot(telekey)
telekeylog = 'TELEGRAM LOG BOT API'
botlog = telepot.Bot(telekeylog)

#Getting bot specification
bot.getMe()

#Initializing the cleverbot
cleverkey = 'CLEVERBOT API'
cb = cleverbot.Cleverbot(cleverkey, timeout=60)
cb.reset()

#Array of sensors raw  data
thermo = [0,0,0,0,0]

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

#ROUNDPOINT
rpoint = 10;

#templimit
sos = 30;

#SOS function
def sosf():
    global thermo
    for i in range (0, 5):
        if (thermo[i] > sos):
            sms(296211623, 'SOS! Sensor #{} measurement is higer than {} °C'.format(i+1, sos))

#round up
def pround(arg):
    return math.ceil(arg*rpoint)/rpoint

# Send message from bot
def sms(ID, str):
    bot.sendMessage(ID, str)

# Send meessage with delay
def sms_delay(sec, ID, strg):
    sleep(DELAY)
    sms(ID, strg) 

thermo = [2,2,2,2,2]
#Getting data
def getraw():
    global thermo
    thermo = [read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)]

#getting raw in background
#def getrawback():
#    temp = threading.Thread(target=getraw)
#    temp.start()

#Sleep function
def sleep(secs):
    time.sleep(secs)

#Success sms
def success(name):
    print ('Success!')
    thread.start_new_thread(botlog.sendMessage, (296211623, 'Success! {}'.format(name).encode('utf-8')))

#The whole data printing function
def temp(ID, thermo):
    humidity = pround(sense.get_humidity())
    pressure = pround(sense.get_pressure())
    
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

#BOTLOG messages
def smslog(user_id, name, command):
    botlog.sendMessage(296211623, '[ {} ] {} : {}'.format(user_id, name, command))
    botlog.sendMessage(319139704, '[ {} ] {} : {}'.format(user_id, name, command))

#BOTLOG background
#def smslogthread(user_id, name, command):
#    tred = threading.Thread(target=smslog, args=(user_id, name, command))
#    tred.start()

#Handling the messages
def handle(msg):
    #chat_id = msg['chat']['id']
    user_id = msg['from']['id']
    name = msg['chat']['first_name'].encode('utf-8')
    #lastname = msg['chat']['last_name']
    command = msg['text'].encode('utf-8')
    print ('[ {} ] {} : {}'.format(user_id, name, command))
    thread.start_new_thread(smslog, (user_id, name, command))
    #smslogthread(user_id, name, command)
    #sms(user_id, cb.interaction_count)

    #START
    if command == '/start':
        try:
            thread.start_new_thread(sms, (user_id, 'Thank you for activating the bot!\n\
This bot is under construction, sometimes it can be offline.\n\
Please type /help to get a list of commands.\n\
Again thanks for trying out the bot and\n\
Have a nice day!' ))
            success(name)
        except:
            print('Exception caught!')
        return
    
    #HUMIDITY
    if command == '/gethumidity':
        try:
            humidity = pround(sense.get_humidity())
            thread.start_new_thread(sms, (user_id, 'Humidity : {} %rH'.format(humidity)))
            success(name)
        except:
            print('Exception caught!')
        return

    #PRESSURE
    if command == '/getpressure':
        try:
            pressure = pround(sense.get_pressure())
            thread.start_new_thread(sms, (user_id, 'Pressure : {} Millibars'.format(pressure)))
            success(name)
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
/help to get this help screen\n\
/time to get current time (local)\n'))
            success(name)
	except:
            print('Exception caught!')
        return

    #TIME
    if command == '/time':
        try:
            now = datetime.now()
            thread.start_new_thread(sms, (user_id, 'Time - {}:{}'.format(now.hour, now.minute)))
            success(name)
        except:
            print('Exception caught!')
        return

    #RESETDUMMT
    if command == '/reset':
        try:
            thread.start_new_thread(sms, (user_id, 'Dont you dare! Ill call SkyNet!'))
            success(name)
        except:
            thread.start_new_thread(sms, (user_id, 'Server didn\'t respond!\nPlease try again.'))
            print('Exception caught!')
        return
      
    #RESETBOT
    if command == '/resetbot':
        try:
            cb.reset()
            thread.start_new_thread(sms, (user_id, 'Bot has been reseted successfully!'))
            success(name)
        except:
            print('Exception caught!')
        return
    
    #SENSORSRAW
    #thermo= [read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)]
    
    #FULL DATA
    if command == '/get':
        try:
            thread.start_new_thread(temp, (user_id, thermo))
            success(name)
    	except:
            print('Exception caught!')
        return

    #TEMPERATURE
    if command == '/gettemp':
        try:
            aver = (thermo[0]+thermo[1]+thermo[2]+thermo[3]+thermo[4])/5
            averround = pround(aver)
            thread.start_new_thread(sms, (user_id, 'Temperature : {} °C'.format(averround)))
            success(name)
        except:
            print('Exception caught!')
        return        

    #CONTROL
    #if command == 'take':
    #    global respond
    #   if respond:
    #        respond = False
    #    if not respond:
    #        respond = True
    #    return

    #BOT RESPONSE
    try:
        response = cb.say(command).encode('utf-8')
        thread.start_new_thread(sms, (user_id, response))
        print ('SandyPI: {}'.format(response))
        thread.start_new_thread(botlog.sendMessage, (296211623, '[ 123456789 ] SandyPI: {}'.format(response)))
        thread.start_new_thread(botlog.sendMessage, (319139704, '[ 123456789 ] SandyPI: {}'.format(response)))
    except:
        thread.start_new_thread(sms, (user_id, 'Server didn\'t respond!\nPlease try again.'))
        print('Exception caught!')

    #SAVE TO FILE
    with open('SPI.txt', 'a') as file:
        now = datetime.now()
        file.write('[{}:{}] {} : {}\n'.format(now.hour, now.minute, name, command))
        file.write('[{}:{}] SandyPI: {}\n'.format(now.hour, now.minute, response))

#bot.getUpdates(timeout=50)    
#bot.message_loop(handle), it's multithreading
MessageLoop(bot, handle).run_as_thread()
#bot.getUpdates(timeout=5)
#OrderedWebhook(bot, handle).run_as_thread()

while 1:
    #thermo= [read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)]
    #getrawback()
    thread.start_new_thread(getraw, ())
    thread.start_new_thread(sosf, ())
    #bot.getUpdates()
    #for i in range (0, 4):
    #    if (thermo[i] > sos):
    #        sms(296211623, 'SOS! Sensor #{} measurement is higer than {} °C'.format(i+1, sos))
    time.sleep(8)
