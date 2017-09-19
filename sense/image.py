from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()
for i in range (1, 100):
    sense.load_image("pics/1.png")
    time.sleep(0.5)
    sense.load_image("pics/2.png")
    time.sleep(0.5)
    sense.load_image("pics/3.png")
    time.sleep(0.5)
