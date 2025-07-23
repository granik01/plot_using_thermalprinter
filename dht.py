import Adafruit_DHT
import time
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def get_temp_humidity():
	humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
	if humidity is not None and temperature is not None:
		print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
		return temperature,humidity 
	else:
		print("Sensor failure. Check wiring.")
		return 0,0

