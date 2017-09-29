#I think this is my first script for raspberry pi
#this just sends some current to i pin for 10 seconds and the turns off
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
i = input("INPUT PIN. IT WILL BE ON FOR 10 SECONDS")
GPIO.setup(i, GPIO.OUT)
GPIO.output(i, True)
time.sleep(10)
GPIO.output(i, False)
GPIO.cleanup()
