import os
import glob
import time
#import telepot
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
#bot = telepot.Bot('439816740:AAGUv-uFga0Vf7XX9-yTPADabX6Eiuf_Bwg')
#bot.getMe()

def read_temp_raw(ORDER):
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[ORDER]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
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

#def handle(msg):
#	chat_id = msg['chat']['id']
#	command = msg['text']
#	print 'Got command: %s' % command
#
#	if command == '/hello':
#		bot.sendMessage(296211623, 'First - {}C\nSecond - {}C\nThird - {}C\nFourth - {}C\nFifth - {}C'.format(read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)))

print(read_temp(0))
print(read_temp(2))
print(read_temp(4))
print(read_temp(3))
print(read_temp(1))
#bot.sendMessage(296211623, 'First - {}C\nSecond - {}C\nThird - {}C\nFourth - {}C\nFifth - {}C'.format(read_temp(0), read_temp(2), read_temp(4), read_temp(3), read_temp(1)))
