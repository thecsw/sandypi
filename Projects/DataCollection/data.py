import os
import glob
import sys
import time
from datetime import datetime
from sense_hat import SenseHat
import thread

sense = SenseHat()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

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

thermo = [0,0,0,0,0]

def getraw():
    global thermo
    thermo = [read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)]

with open('temps.txt', 'a') as file:
    file.write('START.\n')
with open('humidity.txt', 'a') as file:
    file.write('START.\n')
with open('pressure.txt', 'a') as file:
    file.write('START.\n')

for i in range(0, 720):
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    thread.start_new_thread(getraw, ())
    tempaver = (thermo[0]+thermo[1]+thermo[2]+thermo[3]+thermo[4])/5
    with open('temps.txt', 'a') as file:
        file.write("{}\n".format(tempaver))
    with open('humidity.txt', 'a') as file:
        file.write("{}\n".format(humidity))
    with open('pressure.txt', 'a') as file:
        file.write("{}\n".format(pressure))
    time.sleep(120)   
    