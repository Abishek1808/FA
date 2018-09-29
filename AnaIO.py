import time
import Adafruit_ADS1x15
import os
adc=Adafruit_ADS1x15.ADS1015()
try:
        while True:
                Aval1=adc.read_adc(0,2)
		Aval2=adc.read_adc(1,2)
                print 'Analog IN1='+str(Aval1)+"     Analog IN2="+str(Aval2)
                time.sleep(0.5)
except KeyboardInterrupt:
         print('Test Cancelled')

