import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
try:
        while True:
                GPIO.output(10,1)
                GPIO.output(11,0)
                time.sleep(1)
                GPIO.output(10,0)
                GPIO.output(11,1)
                time.sleep(1)
except KeyboardInterrupt:
        GPIO.cleanup()
