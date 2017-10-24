##################################
# Imports ########################
##################################
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import os.path
import math
import signal
import sys

run = True

def handler_stop_signals(signum, frame):
	global run
	run = False
	GPIO.cleanup()


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


##################################
# Alarm class ####################
##################################
class Alarm:
	def __init__(self):
		# Variables

		# Enable alarm
		self.enablePin = 18
		self.alarmEnabled = True
		# Alarm led
		self.ledPin = 20		
		# Alarm states
		self.alarmFired = False
		self.alarmReset = False
		self.alarmLogged = False
		# MQTT
		self.mqttc = mqtt.Client()
		self.mqttc.connect('broker.hivemq.com')
		self.mqttc.subscribe('labo5/controller')
		self.mqttc.on_message = self.on_message
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_subscribe = self.on_subscribe
		
		# Setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.enablePin, GPIO.OUT)
		GPIO.setup(self.ledPin, GPIO.OUT)

		# RPI2
		self.buttons = (27, 22, 16)
		self.previous_input_distance = 0
		self.previous_input_enable = 0
		self.previous_input_reset = 0
		self.requestDistance = False
		self.resetAfter = 5
		GPIO.setup(self.buttons, GPIO.IN, pull_up_down = GPIO.PUD_UP)

		print('ok')

	
	def fireAlarm(self):
		self.alarmFired = True
		self.alarmReset = False
		if self.alarmLogged == False:
			self.postMessageToSlack()
			self.logAlarm()
			self.alarmLogged = True

		# print('Alarm has been fired')

	def resetAlarm(self):		
		self.alarmFired = False
		self.alarmReset = True
		self.alarmLogged = False
		# print('Alarm has been reset')
			
	def blinkRedLed(self):
		if self.alarmFired == True and self.alarmReset == False:
			GPIO.output(self.ledPin, True)
			time.sleep(0.2)
			GPIO.output(self.ledPin, False)
			time.sleep(0.2)

	def alarmStatus(self):
		if self.alarmEnabled == True:
			GPIO.output(self.enablePin, True)
		else:
			GPIO.output(self.enablePin, False)


	# callback functie voor connect event
	def on_connect(self, mqttc, obj, flags, rc):
         print("Connected with result code "+str(rc))

	# callback functie voor subscribe event
	def on_subscribe(self, mqttc, obj, mid, granted_qos):
    	 print('READING')
    	 print("Subscribed: "+str(mid)+" "+str(granted_qos))

    # calback voor het verwerken van de berichten
	def on_message(self, mqttc, obj, msg):
    	 # print("Message Recieved")
    	 try:
            # payload omzetten van bytestring naar string
            p = msg.payload.decode("utf-8")
            
            # json wordt verwacht json string moet omgezet worden naar een python
            #  dictonary voor verwerking
            x = json.loads(p)
            if x["alarmFired"]:
            	self.fireAlarm()
            elif self.requestDistance == True:
            	print("Distance: ", x["distance"], "cm")
            	self.requestDistance = False
            # print(x)
            

            return
    	 except Exception as e:
            print(e)

	def postMessageToSlack(self):
		 from slackclient import SlackClient
		 token = "xoxp-153472905298-152766488672-153473234338-976f66418c71f82104c5a028305752ba"
		 sc = SlackClient(token)
		 resp = sc.api_call(
	        	"chat.postMessage",
	        	as_user="true",
	        	channel="@chinjka",
	        	text="Alarm triggered at " + self.getCurrentTimeStamp()
		 )
		 print("Message has been posted on Slack")

	def getCurrentTimeStamp(self):
	    return time.strftime("%d-%m-%y %H:%M:%S")

	def logAlarm(self):
			self.alarmFiredAt = self.getCurrentTimeStamp()
			f = open('AlarmLog.txt', 'a')
			f.write(self.alarmFiredAt + '\n')
			f.close
			print('Alarm has been logged')

##################################
# RPI 2 ##########################
##################################

	def buttonListeners(self):
		self.enableButtonListener()
		self.resetButtonListener()
		self.distanceButtonListener()
		self.sendDataController()
		time.sleep(0.1)

	def enableButtonListener(self):
	    input1 = not GPIO.input(self.buttons[0])
	    if ((not self.previous_input_enable) and input1):       
	        print('enableButton pressed')
	        self.alarmEnabled = not self.alarmEnabled
	    self.previous_input_enable = input1 

	def resetButtonListener(self):
		# Save the time of initial button press
		self.pressedAt = time.time()
		# While button is pressed, count to 5 sec, then reset the counter and the alarm
		while not GPIO.input(self.buttons[2]) and self.alarmReset == False:
			self.blinkRedLed()		
			print('Alarm will be reset after: ', self.resetAfter - math.floor((time.time() - self.pressedAt)), ' sec')	
			if not (time.time() - self.pressedAt) < self.resetAfter:
				if not self.alarmReset:
					self.resetAlarm()

					# self.reset()


		# 		if ((not self.previous_input_reset) and input2):       
		#     # print('resetButton pressed')
		#     self.alarmReset = True
		# self.previous_input_reset = input2   

	def distanceButtonListener(self):
	    input3 = not GPIO.input(self.buttons[1])
	    if ((not self.previous_input_distance) and input3):       
	        print('distanceButton pressed')
	        self.requestDistance = True
	    self.previous_input_distance = input3

	def sendDataController(self):
		topic = 'labo5/alarm'
		payload = {"alarmEnabled": self.alarmEnabled, "resetAlarm": self.alarmReset, "requestDistance": self.requestDistance}
		# print(payload)
		publish.single(str(topic), json.dumps(payload), hostname="broker.hivemq.com")
		self.alarmReset = False

##################################
# Setup ##########################
##################################
def main():
	try:
		ALARM = Alarm()
		
		while run:	
			if ALARM.alarmEnabled == True:
				if ALARM.alarmFired == False:
					print('Listening to mqtt')
					# ALARM.alarmFired = True
					# ALARM.blinkRedLed()
					
				else:
					ALARM.blinkRedLed()
			ALARM.alarmStatus()
			ALARM.mqttc.loop(0.1)
			# RPI 2
			ALARM.buttonListeners()
    
	except KeyboardInterrupt:
	    pass

	finally:
		GPIO.cleanup()
		print('Exit program')

# main segment
if __name__ == "__main__":
    main()