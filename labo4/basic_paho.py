
# Lab4: leds controlled by mqtt 
# 3 leds connected to pins 18, 23 and 24
# client subscribed to topic "labo/4/basis"
# example of pub: mosquitto_pub -t labo/4/basis -m '{"states": [true, false, false]}'

# Imports
import paho.mqtt.client as mqtt
import json
import time
import RPi.GPIO as GPIO


# tuple object met pin nummers
leds = (18, 23, 24) 
# states = (1, 0, 1)

# initialisatie functie voor leds met als parameter een tuple
def init_leds(leds):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leds, GPIO.OUT)

# set state van de leds met als parameters 2 tuples
# tuple van pin nummers en een met bools van de state
def set_leds(leds, states):
    GPIO.output(leds, states)

# callback functie voor connect event
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

# callback functie voor subscribe event
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

# calback voor het verwerken van de berichten
def on_message(mqttc, obj, msg):
    print("Message Recieved")
    try:
        # payload omzetten van bytestring naar string
        p = msg.payload.decode("utf-8")
        print(p)
        
        # json wordt verwacht json string moet omgezet worden naar een python
        #  dictonary voor verwerking
        x = json.loads(p)
        set_leds(leds, x["states"])
        return
    except Exception as e:
        print(e)


def main():
    try:
        print('Programm started')
        # initialisatie van alle elementen
        init_leds(leds)
        mqttc = mqtt.Client()
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        # mqttc.on_publish = on_publish
        mqttc.on_subscribe = on_subscribe
        mqttc.connect('localhost')
        mqttc.subscribe('labo/4/basis')
        while True:
            mqttc.loop()
                # set_leds(leds, states)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# main segment
if __name__ == "__main__":
    main()
