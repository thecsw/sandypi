import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
i = input("INPUT PIN. IT WILL BE ON FOR 10 SECONDS")
GPIO.setup(i, GPIO.OUT)
GPIO.output(i, True)
time.sleep(10)
GPIO.output(i, False)
GPIO.cleanup()
