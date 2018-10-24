import serial
import binascii
import time
import csv
import paho.mqtt.client as mqtt

ser = serial.Serial()
global NW1_URL
global NW2_URL
def initSerial():
    global ser
    ser.baudrate = 9600
    #ser.port = '/dev/ttyUSB0'
    ser.port = 'COM2'
    #ser.timeout =0
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.rtscts = 0

def get_FromConfig(ConfigName,param):
    with open(ConfigName, 'rU') as infile:
      reader = csv.DictReader(infile)
      data = {}
      for row in reader:
        for header, value in row.items():
          try:
            data[header].append(value)
          except KeyError:
            data[header] = [value]
    return data[param]

def lockVals(request,response,n1_URL,n2_URL):
    if (request[0]=="01"):
        gen_Result(1,request,response,n1_URL)
    if (request[0]=="02"):
        gen_Result(2,request,response,n2_URL)

def gen_Result(slave,request,response,n_URL):
    with open("log.txt", "w+") as log:
        addr=int(request[3],16)
        val=""+response[3]+response[4]
        val=int(val,16)
        result="Request: "+str(request)+" ; Response: "+str(response)+" ; Slave: "+str(slave)+" ; Address :"+str(addr)+" ; TOPIC:"+str(n_URL[addr-1])+" ; Value: "+str(val)
        print(result)
        log.write(result)
def main():
    NW1_URL=get_FromConfig('CONFIG_M1.csv','SENSOR UNIQUE')
    NW2_URL=get_FromConfig('CONFIG_M2.csv','SENSOR UNIQUE')
    rqC=0
    rsC=0
    rqF=0
    rsF=1
    initSerial()
    global ser
    ser.open()
    req=[None]*8
    resp=[None]*7
    tempReq=[None]*8
    while True:
        mHex = ser.read()
        if len(mHex)!= 0:
                ##print("get",binascii.hexlify(bytearray(mHex)))
                if(rqF==0):
                    req[rqC]=(str(binascii.hexlify(bytearray(mHex))))[2:-1]
                    rqC=rqC+1
                    if(rqC==8):
                        tempReq=req
                        req=[None]*8
                        rqC=0
                        rqF=1
                        rsF=0
                        continue
                if(rsF==0):
                    resp[rsC]=(str(binascii.hexlify(bytearray(mHex))))[2:-1]
                    rsC=rsC+1
                    if(rsC==7):
                        lockVals(tempReq,resp,NW1_URL,NW2_URL)
                        resp=[None]*7
                        rsC=0
                        rqF=0
                        rsF=1
                        tempReq=[None]*8
                        continue
        time.sleep(0.1)

try:       
    if __name__ == "__main__":
        main()
except KeyboardInterrupt():
    client.close()
