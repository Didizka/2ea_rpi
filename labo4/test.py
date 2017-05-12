
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO

# tuple object met pin nummers
leds = (18, 23, 24) 
states = (True, False, True)

# initialisatie functie voor leds met als parameter een tuple
def init_leds(leds):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leds, GPIO.OUT)

# set state van de leds met als parameters 2 tuples
# tuple van pin nummers en een met bools van de state
def set_leds(leds, states):
    GPIO.output(leds, states)

init_leds(leds)

while True:
	set_leds(leds, states)