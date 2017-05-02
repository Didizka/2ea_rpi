#import GPIO & time
import RPi.GPIO as GPIO
import time

#name pins by their BCM number
GPIO.setmode(GPIO.BCM)

#Set pin 18 as output
GPIO.setup(18, GPIO.OUT)


#Never ending loop
while (True):
	GPIO.output(18, True)
	time.sleep(1)
	GPIO.output(18, False)
	time.sleep(1)
