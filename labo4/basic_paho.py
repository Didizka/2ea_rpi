
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO

# tuplje object met pin nummers
leds = (5, 6, 13) 

# initialisatie functie voor leds met als parameter een tuple
def init_leds(leds):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leds, GPIO.OUT)

# set state van de leds met als parameters 2 tuples
# tuple van pin nummers en een met bools van de state
def set_leds(leds, states):
    GPIO.output(leds, states)

# calback voor het verwerken van de berichten
def on_message(mqttc, obj, msg):
    print("Message Recieved")
    try:
        # payload omzetten van bytestring naar string
        p = msg.payload.decode("utf-8")
        
        # json wordt verwacht json string moet omgezet worden naar een python
        #  dictonary voor verwerking
        x = json.loads(p)

        #
        set_leds(leds, tuple(x['leds']))
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
	    mqttc.connect("127.0.0.1")
	    mqttc.subscribe('tmp')
	    while True:
                mqttc.loop()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# main segment
if __name__ == "__main__":
    main()