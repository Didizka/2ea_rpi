#import GPIO & time
import RPi.GPIO as GPIO
import time

#name pins by their BCM number
GPIO.setmode(GPIO.BCM)

#Set pin 24 as output and 23 as input
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.IN)


#Never ending loop
while (True):
	GPIO.output(24, False)

	input = GPIO.input(23)
	
	if (input == True):
		GPIO.output(24, False)
	else:
		GPIO.output(24, True)
