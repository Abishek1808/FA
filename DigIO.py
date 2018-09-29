import time
import RPi.GPIO as pin
import os
pin.setmode(pin.BCM)
pin.setup(22,pin.IN)
pin.setup(27,pin.IN)
print "----------------------------HIT Ctrl+C anytime to terminate-----------------------------------"
try:
        while 1:
                d1val=pin.input(22)
                d2val=pin.input(27)
                print 'D1 IN  ='+str(d1val)+',   D2 IN  ='+str(d2val)
                time.sleep(0.5)
except KeyboardInterrupt:
         print('Test Cancelled')


