##################################
# Imports ########################
##################################
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import os.path
import math
import json


##################################
# Counter class ####################
##################################
class Counter:
	def __init__(self):
		# Variables

		self.btnPin = 17
		self.ledPin = 18
		self.personCount = 0	
		self.currentPwm = 0
		self.previous_input = 0
		self.sendAndSaveAfter = 5
			
		
		# MQTT
		self.mqttc = mqtt.Client()
		self.mqttc.connect("localhost")
		self.mqttc.subscribe("examen")
		self.mqttc.on_message = self.on_message
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_subscribe = self.on_subscribe
		
		# Setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.btnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(self.ledPin, GPIO.OUT)		
		self.pwm = GPIO.PWM(self.ledPin, 100)
		self.pwm.start(0)
		print('Counter initialized')



	# callback functie voor connect event
	def on_connect(self, mqttc, obj, flags, rc):
         print("Connected with result code "+str(rc))

	# callback functie voor subscribe event
	def on_subscribe(self, mqttc, obj, mid, granted_qos):
    	 print('READING')
    	 print("Subscribed: "+str(mid)+" "+str(granted_qos))

    # calback voor het verwerken van de berichten
	def on_message(self, mqttc, obj, msg):
		try:
	        # payload omzetten van bytestring naar string
	    	 payload = msg.payload.decode("utf-8")
	    	 if (payload == "send"):
	    	 	self.sendDataCounter()
	    	 # print(p)
	    	 return
		except Exception as e:
	    	 print(e)

	def sendDataCounter(self):
		f = open('person_count.txt', 'r')
		count = f.read()
		f.close()
		topic = 'examen'
		payload = {"person_count": count}
		publish.single(str(topic), json.dumps(payload), hostname="localhost")
		print('Counter has been sent over MQTT')

	def ledCounterDisplay(self):
		self.currentPwm = (self.personCount % 10) * 10
		self.pwm.ChangeDutyCycle(self.currentPwm)	

	def btnListener(self):
		pressedAt = time.time()
		input = not GPIO.input(self.btnPin)

		# 5 sec press
		while not GPIO.input(self.btnPin):	
			# print('Alarm will be reset after: ', self.sendAndSaveAfter - math.floor((time.time() - pressedAt)), ' sec')	
			duration = time.time() - pressedAt
			if not duration < self.sendAndSaveAfter:
				self.log()
				self.sendDataCounter()

		
		# Single press
		if ((not self.previous_input) and input):       
	         self.increasePersonCounter();
		self.previous_input = input   
		time.sleep(0.1)


	def increasePersonCounter(self):
		self.personCount = self.personCount + 1
		print("Current counter: ", self.personCount)

	def log(self):
		f = open('person_count.txt', 'w')
		f.write(str(self.personCount))
		f.close
		print('Person counter has been logged')

##################################
# Setup ##########################
##################################
def main():
	try:
		COUNTER = Counter()
		
		while True:	
			COUNTER.ledCounterDisplay()
			COUNTER.btnListener()
			COUNTER.mqttc.loop(.1)
    
	except KeyboardInterrupt:
	    pass

	finally:
		GPIO.cleanup()
		print('Exit program')

# main segment
if __name__ == "__main__":
    main()