import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
print "Sending On Signal to UC20"
GPIO.output(19,True)
time.sleep(0.7)
GPIO.output(19,False)
print "Done" ## When loop is complete, print "Done"
GPIO.cleanup()




