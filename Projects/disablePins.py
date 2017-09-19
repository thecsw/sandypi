import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

for i in range (2, 27):
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, False)
GPIO.cleanup()
