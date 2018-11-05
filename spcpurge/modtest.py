import pymodbus
import sys
import serial
import paho.mqtt.client as mqtt
import time
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize$
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

sa=int(sys.argv[1])
ln=int(sys.argv[2])
id=int(sys.argv[3])

client= ModbusClient(method = "rtu", port="/dev/ttyUSB0",stopbits = 1, bytesize$
while True:
        connection = client.connect()
        print connection
        result= client.read_holding_registers(sa,ln,unit= id)
        print (result.registers)
        val=result.registers[1]
        val1=result.registers[2]
        print(val)
        print (val1)
        client.close()
        #mClient.publish("FaTEST/CHANNELA",a)
        #Client.publish("FaTEST/CHANNELB",b)
        val=int(val)
        val=float(val/16)
        val=(val*500)/(200*16*4095)
        print ("pressure ======"+str(val))


