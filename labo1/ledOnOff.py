
#Import modules
import RPi.GPIO as GPIO
import time

#Define variables
buttonPin = 26
ledPin = 20
ledOn = False
previous_input = 0


#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ledPin, GPIO.OUT)


#Loop
while (True):
	#get current input from the button
	input = GPIO.input(buttonPin)

	#if button is pressed check previous button state
	if ((not previous_input) and input):		
		#turn the led ON/OFF
		GPIO.output(ledPin, ledOn)
		ledOn = not ledOn
	
	#Save last button state
	previous_input = input

	#Wait some tome to debounce the button
	time.sleep(0.05)
	