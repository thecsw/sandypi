#SandyMalina
#Code for the rgb light thingy
import RPi.GPIO as GPIO
import sys
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BLUE = 18
GREEN = 15
RED = 14
MYPI = 4
SLEEP = 0.5
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(MYPI, GPIO.OUT)
time.sleep(5)
#Setup is over

def OUTPUT (COLOR):
    GPIO.output(COLOR, True)
    time.sleep(SLEEP)
    GPIO.output(COLOR, False)
    return

def MULTOUTPUT (COLOR, COLORS):
    GPIO.output(COLOR, True)
    GPIO.output(COLORS, True)
    time.sleep(SLEEP)
    GPIO.output(COLOR, False)
    GPIO.output(COLORS, False)
    return

def MMULTOUTPUT (COLOR, COLORS, COLORSS):
    GPIO.output(COLOR, True)
    GPIO.output(COLORS, True)
    GPIO.output(COLORSS, True)
    time.sleep(SLEEP)
    GPIO.output(COLOR, False)
    GPIO.output(COLORS, False)
    GPIO.output(COLORSS, False)
    return

def SRED ():
    OUTPUT(RED)
    return

def SGREEN ():
    OUTPUT(GREEN)
    return

def SBLUE ():
    OUTPUT(BLUE)
    return

def SPURPLE ():
    MULTOUTPUT (RED, BLUE)
    return
    
def SLIME ():
    MULTOUTPUT (RED, GREEN)
    return

def LBLUE ():
    MULTOUTPUT (GREEN, BLUE)
    return

def WHITE ():
    MMULTOUTPUT(RED, GREEN, BLUE)

def SHUTDOWN ():
    GPIO.output(RED, False)
    GPIO.output(GREEN, False)
    GPIO.output(BLUE, False)
    return

while True:
    while GPIO.input(MYPI): 
            SRED()
            SGREEN()
            SBLUE()
            SLIME()
            LBLUE()
            SPURPLE()
            WHITE()
    time.sleep(1)

SHUTDOWN()
GPIO.cleanup()
