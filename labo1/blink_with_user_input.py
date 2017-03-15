#import GPIO & time
import RPi.GPIO as GPIO
import time

#name pins by their BCM number
GPIO.setmode(GPIO.BCM)

#Set pin 18 as output
GPIO.setup(18, GPIO.OUT)

#Ask user for on and off time
on = raw_input("Enter ON time: ")
off = raw_input("Enter OFF time: ")

#Never ending loop
while (True):
	GPIO.output(18, True)
	time.sleep(float(on))
	GPIO.output(18, False)
	time.sleep(float(off))
