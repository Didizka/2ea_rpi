##################################
# Imports ########################
##################################
import RPi.GPIO as GPIO
import time
import os.path
import math

##################################
# Alarm class ####################
##################################


class Alarm:
	def __init__(self):
		# Enable alarm
		self.enablePin = 18
		self.alarmEnabled = False
		self.previous_input = 0
		# Button
		self.buttonPin = 26
		# Alarm led
		self.ledPin = 20		
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
			f = open('AlarmLog.txt', 'a')
			f.write(self.alarmFiredAt + '\n')
			f.close


	def detectReset(self):
		# Save the time of initial button press
		self.pressedAt = time.time()
		# While button is pressed, count to 5 sec, then reset the counter and the alarm
		while not GPIO.input(self.buttonPin) and self.alarmReset == False:
			self.blinkRedLed()		
			print('Alarm will be reset after: ', self.resetAfter - math.floor((time.time() - self.pressedAt)), ' sec')	
			if not (time.time() - self.pressedAt) < self.resetAfter:
				if not self.alarmReset:
					print("Alarm has been reset")
					self.reset()
				

	def reset(self):		
		self.alarmFired = False
		self.timeStampLogged = False
		self.alarmReset = True

	def enableAlarm(self):
		input = not GPIO.input(self.enablePin)
		if ((not self.previous_input) and input):		
			self.alarmEnabled = not self.alarmEnabled
			self.reset()
		previous_input = input
		time.sleep(0.1)
		

##################################
# Setup ##########################
##################################
def main():
	try:
		ALARM = Alarm()
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(ALARM.buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(ALARM.enablePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(ALARM.ledPin, GPIO.OUT)
		GPIO.setup(ALARM.trigger, GPIO.OUT)
		GPIO.setup(ALARM.echo, GPIO.IN)
		# Ensure the trig pin is low
		GPIO.output(ALARM.trigger, False)
		print('ok')

		while True:	
			# If no alarm was fired, measure the distance until the door is opened
			# if it was opened, fire alarm
			# Log timestamp of alarm
			# blink red leds
			ALARM.enableAlarm()
			if ALARM.alarmEnabled == True:		
				if ALARM.alarmFired == False:
					ALARM.measure()		
				else:			
					if ALARM.timeStampLogged == False:
						print('alarm fired at: ', ALARM.alarmFiredAt)	
						ALARM.timeStampLogged = True
					ALARM.blinkRedLed()
					ALARM.detectReset()		
			else:
				print('Alarm disabled')
			time.sleep(0.1)
    
	except KeyboardInterrupt:
	    pass
	finally:
		GPIO.cleanup()
		print('Exit program')

# main segment
if __name__ == "__main__":
    main()


