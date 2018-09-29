from threading import Thread
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import os
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(19, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

def dialPPP0():
        os.system('sudo wvdial 3gconnect')

def setdef():
        time.sleep(10)
        os.system('sudo route add default gw 10.64.64.64')

def myProg():
        time.sleep(12)
        os.system('sudo python testConnec.py')


def Main():
        t1=Thread(target=dialPPP0)
        t2=Thread(target=setdef)
        t3=Thread(target=myProg)
        print "Sending On Signal to UC20"
        GPIO.output(19,True)
	time.sleep(0.15)
        GPIO.output(19,False)
        GPIO.cleanup()
        print "Done" ## When loop is complete, print "Done"
        time.sleep(10)
        t2.start()
        #t3.start()
        t1.start()

Main()


