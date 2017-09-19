from sense_hat import SenseHat
import time

sense = SenseHat()
#for i in range(1, 10):
while True:
	print("Temperature from temperature sensor: %s" % sense.get_temperature())
	print("Temparature from humidity sensor: %s" % sense.get_temperature_from_humidity())
	print("Temperature from pressure sensor: %s" % sense.get_temperature_from_pressure())

	print("Humidity: %s %%rH" % sense.get_humidity())
	print("Pressure: %s Milibars" % sense.get_pressure())
	time.sleep(2)
