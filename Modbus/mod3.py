import serial
from serial import rs485
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

#PORT = 1
PORT = '/dev/ttyAMA0'
socket=serial.rs485.RS485(port=PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
socket.rs485_mode= serial.rs485.RS485Settings(rts_level_for_tx=True, rts_level_for_rx=False, loopback=False, delay_before_tx=None, delay_before_rx=None)

def main():
    """main"""
    logger = modbus_tk.utils.create_logger("console")

    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(socket)
        master.set_timeout(5.0)
        master.set_verbose(True)
        logger.info("connected")

        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 1, 3))

        #send some queries
        #logger.info(master.execute(1, cst.READ_COILS, 0, 10))
        #logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 8))
        #logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 100, 3))
        #logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 12))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 7, output_value=1))
        #logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=54))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 0, 1, 1, 0, 1, 1]))
        #logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12)))

    except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())

if __name__ == "__main__":
    main()
