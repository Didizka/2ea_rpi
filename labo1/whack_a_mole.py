

#Import modules
import RPi.GPIO as GPIO
import time

#Define variables
buttonPin = 17
ledPins = [18, 19, 20, 21, 22]
interval = 1.0
decreaseWith = 0.3
currentLed = 0

#Functions
def initLeds():
        for i in range(len(ledPins)):
                GPIO.setup(ledPins[i], GPIO.OUT)        

def lightLed(num):
        for i in range(len(ledPins)):
                if i == num:
                        GPIO.output(ledPins[i], True)
                else:
                        GPIO.output(ledPins[i], False)

def cycleLeds():
        global currentLed
        lightLed(currentLed)
        currentLed += 1
        if currentLed == len(ledPins):
                currentLed = 0
        time.sleep(interval)

# buttonPin interrupt callback function
def speedUp(buttonPin):
        global interval
        if (interval - decreaseWith > 0):
                if GPIO.input(ledPins[2]):
                        interval -= decreaseWith
                        print "Interval decreased. Current interval ", interval
                else:
                        print "Middle led not lighted"
        else:
                print "Congratz! Max speed reached"

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
initLeds()
GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=speedUp, bouncetime=200)

#Loop
while (True):
        cycleLeds()
        



