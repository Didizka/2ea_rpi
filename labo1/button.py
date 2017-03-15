import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

gpio.setup(23, gpio.IN)

while True:
	input = gpio.input(23)
	if input == True:
		print("Button pressed")
		time.sleep(0.2)
