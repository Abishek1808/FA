import sys
#from urllib.request import urlopen
#import requests
import os
import serial
from threading import Thread
from collections import defaultdict
import time
from time import strftime
import datetime
import calendar
import paho.mqtt.client as mqtt
import csv
import pymodbus
import redis
from multiprocessing import Process, Queue
import modbus_tk.defines as cst
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.sync import ModbusTcpClient as ModbusClient


#client = ModbusClient(method='rtu', port=porta,timeout=2, parity='E', stopbits=1, baudrate=9600, unit=1)
client = ModbusClient('localhost', port=502, timeout=2, parity='E', baudrate=9600, unit=1)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
now = datetime.datetime.now()
sendTime = now.replace(hour=23, minute=45, second=0, microsecond=0)
start=1

min_sysPres=0
max_sysPres=6
min_maniPres=0
min_maniPres=6
min_difPres=0
max_difPres=50
maniThreshold=3

hopperCount=4


def convertDiffPres(curVal):
    curVal=float(curVal/100)
    p=float((((max_difPres-min_difPres)/16)*(curVal-4))+min_difPres)
    return p

def convertSysPres(curVal):
    curVal=float(curVal/100)
    p=float((((max_sysPres-min_sysPres)/16)*(curVal-4))+min_sysPres)
    return p

def convertManiPres(curVal):
    curVal=float(curVal/100)
    p=float((((max_maniPres-min_maniPres)/16)*(curVal-4))+min_maniPres)
    return p


def get_FromConfig(param):
    with open('OnlinePurgeConfig.csv', 'rU') as infile:
      reader = csv.DictReader(infile)
      data = {}
      for row in reader:
        for header, value in row.items():
          try:
            data[header].append(value)
          except KeyError:
            data[header] = [value]
    return data[param]

def get_maniPressure(I):
    client.connect()
    print ("Reading ManiPres   " +str(ID))
    rp = client.read_holding_registers(1,10, unit=ID)
    client.close()
    pressure=rp.registers
    pressure=int(pressure[0])
    pressure=convertManiPres(pressure)
    maniRef = 'mP'+str(I)
    redis.set(maniRef,pressure)
    return pressure

def get_IVStat(I):
    ID=ivStartID+I
    rr = client.read_holding_registers(44, 2, unit=ID)
    client.close()
    stat=rr.bits
    stat=int(stat[1])
    stat="{0:b}".format(stat)
    binVals=list(stat)
    stat=binVals[10]
    coilRef='IV'+str(I)
    redis.set(coilRef,stat)
    print ( coilRef+" :"+str(stat))
    return stat
    
def convert_Toint(arr):
    for i in range (len(arr)):
        print (arr[i])
        arr[i]=int(arr[i])
    return arr

def convertArr_Toint(arr):
    for i in range (len(arr)):
        print (arr[i])
        kk=arr[i].split(',')
        arr[i]=kk
    for i in range (len(arr)):
        for j in range (len(arr[i])):
            arr[i][j]=int(arr[i][j])
    return arr

def getMasterpressureData():
    client.connect()
    rr = client.read_holding_registers(1, 10, unit=99)
    client.close()
    pressure=rr.registers
    systemPres=int(rr.registers[0])
    pressure=int(pressure[1])
    bbd1=int(rr.registers[2])
    bbd2=int(rr.registers[3])
    bbd3=int(rr.registers[4])
    bbd4=int(rr.registers[5])
    inletTemp=int(rr.registers[6])
    reds.set('SysPsi',systemPres)
    redis.set('dp',pressure)
    return pressure

def bgsystemMonitor():
    getMasterpressureData()
    time.sleep(0.5)
    

def writeCoilTrue(Id,add):
    client.connect()
    rcl=client.write_coils(add,True,unit=Id)
    client.close()

def writeCoilFalse(Id,add):
    client.connect()
    rcl=client.write_coils(add,True,unit=Id)
    client.close()

def gen_writeCoilSeq(valv): # compartments,Manifolds,Valvespermanifolds
    IDseq=[]
    k=0
    ot=0
    id=0
    oTT=[]
    IDA=[]
    for i in range (len(valv)):
        temp=[]
        ot=ot+1
        idArrtemp=[]
        for j in range (len(valv[i])):
            id=id+1
            oTT.append(ot)
            k=0
            for h in range (valv[i][j]):
                k=k+1
                idArrtemp.append(id)
                temp.append(k)
        IDA.append(idArrtemp)
        IDseq.append(temp)
    fin=[]
    finID=[]
    maxi=max(IDseq,key=len)
    print ('maxi   '+str(maxi))
    for i in range (len(maxi)):
        try:
            for j in range (len(maxi)):
                fin.append(IDseq[j][i])
                finID.append(IDA[j][i])
        except IndexError:
            a=0
    return fin,finID

def get_startStatus():
    return int(redis.get('st'))



def monitor_ManifoldPres(I):
    ##monitor drop till 2.4 and raise to 3

def initializePurge(Valve,Manifold,MinPres):
    for i in range (len(Manifold)):
            update_hopper()
            if(getMasterpressureData()>MinPres and get_startStatus()==1):
                if(get_IVStat(Manifold[i])==1 and get_maniPressure(Manifold[i])==maniThreshold ):
                    print ("purging manifold"+str(Manifold[i])+"---valve"+str(Valve[i]))
                    writeCoilTrue(Manifold[i],Valve[j])
                    time.sleep(2)
                    #writeCoilFalse(i,j)
def update_hopper():
    start=101
    hopperTempRef="H_Temp"
    for i in range (1,hopperCount):
        rr=client.read_holding_registers(1,10,unit=i)
        temp=rr.registers[0]
        hopperTempRef=hopperTempRef+str(i)
        redis.set(hopperTempRef,temp)
    

maxThreshold=20     ###get_maniPressure(Manifold[i])==3 and 
minThreshold=15     ###
compartments=2      ###
manifolds=[1,2,3,4] ###
vPmf=[4,4,4,4]  ### 


try:
    compartments=get_FromConfig('COMPARTMENTS')
    manifolds=get_FromConfig('MANIFOLDS')
    vPmf=get_FromConfig('VALVES')
    maxThreshold=get_FromConfig('THRESHOLD MAX')
    minThreshold=get_FromConfig('THRESHOLD MIN')
    #compartments=convert_Toint(compartments)
    #manifolds=convert_Toint(manifolds)
    vPmf=convertArr_Toint(vPmf)
    maxThreshold=int(maxThreshold[0])
    minThreshold=int(minThreshold[0])
    print ("MMMMMMTTTTTTTTT   "+str(maxThreshold))
    print ("mmmmmmttttttttttt   "+str(minThreshold))
    IDarray,ManifoldOrd=gen_writeCoilSeq(vPmf)
    MasterScan = Process(target=bgsystemMonitor)
    MasterScan.start()
    while True:
        #start=int(redis.get('st'))
        pressure=getMasterpressureData()
        print (' Normal Operation pressure  :' + str(pressure)+" ; maxT  :"+str(maxThreshold))
        while(get_startStatus()==1):
            if( getMasterpressureData() >= maxThreshold):
                    print ('initializing purging sequence')
                    initializePurge(IDarray,ManifoldOrd,minThreshold)
            else:
                print ('Scanning pressure pressure normal')
            time.sleep(2)
        time.sleep(2)
                       
except KeyboardInterrupt:
    MasterScan.stop()
    client.close()


    
