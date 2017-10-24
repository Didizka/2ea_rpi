
#Import modules
import RPi.GPIO as GPIO
import time

#Define variables
buttonPin = 17
ledPin = 18
ledOn = False
previous_input = 0


#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ledPin, GPIO.OUT)
pwm = GPIO.PWM(ledPin, 100)
currentPwm = 0
pwm.start(0)

#Loop
while (True):
	#get current input from the button
	input = GPIO.input(buttonPin)

	#if button is pressed check previous button state
	if ((not previous_input) and input):		
		#increase currentPwm with 10% with each button press
		# when CurrentPwm reaches 100%, reset it back to 0
		if currentPwm == 100:
			currentPwm = 0
		pwm.ChangeDutyCycle(currentPwm)		
		currentPwm = currentPwm + 10
	
	#Save last button state
	previous_input = input

	#Wait some tome to debounce the button
	time.sleep(0.05)
	