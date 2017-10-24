
# Lab4: leds controlled by mqtt 
# 3 leds connected to pins 18 and 23
# client subscribed to topic "labo/4/basis"
# example of local pub: mosquitto_pub -t labo/4/basis -m '{"states": [true, false]}'
# via online broker: mosquitto_pub -h broker.hivemq.com -p 1883 -t labo/4/basis -m '{"states" : [true, true]}'
# Chingiz: sub: 'home/groundfloor/kitchen/lights/lightx'
#          pub: 'home/groundfloor/livingroom/lights/lightx'
# Lander: omgekeerd

# Imports
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time
import RPi.GPIO as GPIO


class Labo4:
    def __init__(self):     
        # tuple object met pin nummers
        self.leds = (18, 23) 
        self.buttons = (27, 22)
        self.led1state = False
        self.led2state = False
        self.states = [self.led1state, self.led2state] 
        self.previous_input1 = 0
        self.previous_input2 = 0

        # Disable button
        self.disableButton = 17
        self.previous_input = 0
        self.isDisabled = False

        # Pins setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.leds, GPIO.OUT)
        GPIO.setup(self.disableButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.buttons, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def disableButtonListener(self):
        input = not GPIO.input(self.disableButton)
        if ((not self.previous_input) and input):       
            self.isDisabled = not self.isDisabled
        self.previous_input = input  
        # if self.isDisabled:
            # self.disableLeds()      
        # time.sleep(0.1)


    def disableLeds(self):
        GPIO.output(self.leds, False)
        # print('Leds are disabled')

    def stateButtonListeners(self):
        # self.states[0] = not GPIO.input(self.buttons[0])
        # self.states[1] = not GPIO.input(self.buttons[1]) 

        input1 = not GPIO.input(self.buttons[0])
        if ((not self.previous_input1) and input1):       
            self.led1state = not self.led1state
        self.previous_input1 = input1 
        # time.sleep(0.1)

        input2 = not GPIO.input(self.buttons[1])
        if ((not self.previous_input2) and input2):       
            self.led2state = not self.led2state
        self.previous_input2 = input2 
        # time.sleep(0.1)


        topic = 'home/groundfloor/kitchen/lights/lightx'
        payload = {"states" : [self.led1state, self.led2state], "master" : self.isDisabled}       
        # print(topic)
        # print(payload)
        publish.single(str(topic), json.dumps(payload), hostname="172.16.229.39")

    # set state van de leds met als parameters 2 tuples
    # tuple van pin nummers en een met bools van de state
    def set_leds(self, leds, states):
        if not self.isDisabled:
            GPIO.output(self.leds, states)

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
            self.set_leds(self.leds, x["states"])
            master = x["master"]
            if master:
                self.disableLeds()
            return
        except Exception as e:
            print(e)


def main():
    try:
        print('Programm started')   

        # initialisatie van alle elementen
        labo4 = Labo4()    
        
        mqttc = mqtt.Client()
        # mqttc.connect('broker.hivemq.com')
        mqttc.connect('172.16.229.39')
        mqttc.subscribe('home/groundfloor/livingroom/lights/lightx')
        

        mqttc.on_message = labo4.on_message
        mqttc.on_connect = labo4.on_connect
        mqttc.on_subscribe = labo4.on_subscribe
        # local broker
        # mqttc.connect('localhost')
        # online broker

        while True:
            mqttc.loop(.1)
            labo4.disableButtonListener()
            labo4.stateButtonListeners()
            
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# main segment
if __name__ == "__main__":
    main()
