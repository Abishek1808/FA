import modbus_tk
import sys
import time
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import serial
from serial import rs485
pTimeout=0.01
err=0
machineID=1

startReg=1
nbrReg=3
socket = serial.rs485.RS485(port='/dev/ttyAMA0', baudrate=115200, bytesize=8, parity='N', stopbits=1, rtscts=True, dsrdtr=False, timeout=pTimeout, xonxoff=0 )
socket.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=True, rts_level_for_rx=False, loopback=False, delay_before_tx=None, delay_before_rx=None)

#Modbus:******************************

pTimeout = 0.01

master = modbus_rtu.RtuMaster(socket)

master.set_timeout( pTimeout )
master.set_verbose(True)

#Read function:*************************


#----------------------------------------------------------#
def readFromMachine(machineID,startReg,nbrReg, dataArray):
#return newoldreadFromMachine(machineID,startReg,nbrReg, dataArray)
	result = ()
	err = 0
while(err < 1):
	try:
		sys.stdin.flush()
		sys.stdout.flush()
		rr = master.execute(int(machineID), cst.READ_HOLDING_REGISTERS, int(startReg), int(nbrReg))
		result = rr
		if(len(result) > 0 ):
			ii = 0
			for i in range( startReg,startReg + nbrReg ):
				dataArray = result[ii]
				ii = ii + 1
			if(err > 0):
				print('Error: ' + str(err) + ' M=>' + str(machineID) + " Start= " + str(startReg) + " Nbr= " + str(nbrReg) + " Val= " + str(len(rr)) ,9)
#				return result

	except modbus_tk.modbus.ModbusError, e:
		print("r1(" + str(machineID) + ") " + "%s- Code=%d" % (e, e.get_exception_code()),10)
		err = err + 1

	except modbus_tk.modbus_rtu.ModbusInvalidResponseError, e:
		err = err + 1
		print("r2(" + str(machineID) + ") " + "%s- Code=ModbusInvalidResponseError" % (e),10)
#master.close()
#socket.close()
#sys.stdin.flush()
#sys.stdout.flush()
#time.sleep(0.1)
		time.sleep((nbrReg) * 2 / 1000);
#		return result
'''except :
#master.close()
#socket.close()
#sys.stdin.flush()
#sys.stdout.flush()
screenPrinter("(" + str(machineID) + ") " + "oppppppppppppppps (" + str(machineID) + ")" , 10)
err = err + 1
time.sleep(0.001)'''
