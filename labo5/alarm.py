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
		# Distance meter
		self.trigger = 23
		self.echo = 24
		# Fire alarm at 5cm opening
		self.doorOpenedAt = 30
		# MQTT
		self.mqttc = mqtt.Client()
		self.mqttc.connect('broker.hivemq.com')
		self.mqttc.subscribe('labo5/alarm')
		self.mqttc.on_message = self.on_message
		self.mqttc.on_connect = self.on_connect
		self.mqttc.on_subscribe = self.on_subscribe
		
		# Setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.enablePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(self.ledPin, GPIO.OUT)
		GPIO.setup(self.trigger, GPIO.OUT)
		GPIO.setup(self.echo, GPIO.IN)
		# Ensure the trig pin is low
		GPIO.output(self.trigger, False)

		print('ok')

	def measure(self):
		pulse_start = 0
		pulse_end = 0
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
			self.fireAlarm()
			self.blinkRedLed()
			self.sendDataAlarm()

	def fireAlarm(self):
		self.alarmFired = True
		self.alarmReset = False
		# print('Alarm has been fired')

	def resetAlarm(self):		
		self.alarmFired = False
		self.alarmReset = True
		# print('Alarm has been reset')
			
	def blinkRedLed(self):
		if self.alarmFired == True and self.alarmReset == False:
			GPIO.output(self.ledPin, True)
			time.sleep(0.2)
			GPIO.output(self.ledPin, False)
			time.sleep(0.2)

	def alarmStatus(self):
		if self.alarmEnabled:
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
            print(x)
            # alarmReset = x["alarmReset"]
            # if alarmReset:
            # 	self.resetAlarm()
            return
    	 except Exception as e:
            print(e)

	def sendDataAlarm(self):
    	 topic = 'labo5/controller'
    	 payload = {"alarmFired": self.alarmFired}
    	 publish.single(str(topic), json.dumps(payload), hostname="broker.hivemq.com")


##################################
# Setup ##########################
##################################
def main():
	try:
		ALARM = Alarm()
		
		while run:	
			if ALARM.alarmEnabled == True:
				if ALARM.alarmFired == False:
					# ALARM.measure()
					print('ok')
				else:
					ALARM.blinkRedLed()
			ALARM.mqttc.loop(0.1)
    
	except KeyboardInterrupt:
	    pass

	finally:
		GPIO.cleanup()
		print('Exit program')

# main segment
if __name__ == "__main__":
    main()