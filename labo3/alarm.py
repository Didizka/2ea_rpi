##################################
# Imports ########################
##################################
import RPi.GPIO as GPIO
import time

##################################
# Alarm class ####################
##################################

class Alarm:

	def __init__(self):
		# Button
		self.buttonPin = 26
		# Alarm led
		self.ledPin = 20
		# Debounce button
		self.previous_input = 0
		# Alarm states
		self.alarmFired = False
		self.timeStampLogged = False
		self.resetAfter = 5
		self.alarmReset = False
		# Distance meter
		self.trigger = 23
		self.echo = 24
		# Fire alarm at 5cm opening
		self.doorOpenedAt = 5
		

	def getCurrentTimeStamp(self):
	    return time.strftime("%d-%m-%y %H:%M:%S")

	def getCurrentSeconds(self):
		return int(time.time())

	def blinkRedLed(self):
		if self.alarmFired == True and self.alarmReset == False:
			GPIO.output(self.ledPin, True)
			time.sleep(0.2)
			GPIO.output(self.ledPin, False)
			time.sleep(0.2)

	def measure(self):
		GPIO.output(self.trigger, True)
		time.sleep(0.00001)
		GPIO.output(self.trigger, False)

		while GPIO.input(self.echo)==0:
		  pulse_start = time.time()

		while GPIO.input(self.echo)==1:
		  pulse_end = time.time()     

		pulse_duration = pulse_end - pulse_start
		self.distance = pulse_duration * 17150
		self.distance = round(self.distance, 1)

		print("Distance:", self.distance, "cm")

		if self.distance > self.doorOpenedAt:
			self.alarmFired = True
			self.alarmReset = False
			self.alarmFiredAt = self.getCurrentTimeStamp()

	def detectReset(self):
		# Save the time of initial button press
		self.pressedAt = time.time()
		# While button is pressed, count to 5 sec, then reset the counter and the alarm
		while not GPIO.input(self.buttonPin):
			self.blinkRedLed()
			if not (time.time() - self.pressedAt) < self.resetAfter:
				if not self.alarmReset:
					self.reset()
				

	def reset(self):
		print ("Alarm has been reset")
		self.alarmFired = False
		self.timeStampLogged = False
		self.alarmReset = True

		

##################################
# Setup ##########################
##################################
ALARM = Alarm()
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALARM.buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(ALARM.ledPin, GPIO.OUT)
GPIO.setup(ALARM.trigger, GPIO.OUT)
GPIO.setup(ALARM.echo, GPIO.IN)
# Ensure the trig pin is low
GPIO.output(ALARM.trigger, False)


##################################
# Loop ###########################
##################################
while True:	
	# If no alarm was fired, measure the distance until the door is opened
	# if it was opened, fire alarm
	# Log timestamp of alarm
	# blink red leds
	if ALARM.alarmFired == False:
		ALARM.measure()		
	else:			
		if ALARM.timeStampLogged == False:
			print('alarm fired at: ', ALARM.alarmFiredAt)	
			ALARM.timeStampLogged = True
		ALARM.blinkRedLed()
		ALARM.detectReset()

	time.sleep(0.1)
	# print(ALARM.getCurrentSeconds())