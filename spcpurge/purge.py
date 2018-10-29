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
client = ModbusClient('192.168.137.1', port=502, timeout=1, parity='N', baudrate=9600, unit=1)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
now = datetime.datetime.now()
sendTime = now.replace(hour=23, minute=45, second=0, microsecond=0)
start=1

def get_FromConfig(param):
    with open('Configs/OnlinePurgeConfig.csv', 'rU') as infile:
      reader = csv.DictReader(infile)
      data = {}
      for row in reader:
        for header, value in row.items():
          try:
            data[header].append(value)
          except KeyError:
            data[header] = [value]
    return data[param]

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

def getpressureData():
    client.connect()
    rr = client.read_holding_registers(1, 1, unit=50)
    if not hasattr(rr,'registers'):
        print ('recurring---')
        time.sleep(4)
        getmodbusData(rL)
    client.close()
    pressure=rr.registers
    pressure=int(pressure[0])
    redis.set('dp',pressure)
    return pressure

def writeCoilTrue(Id,add):
    client.connect()
    rcl=client.write_coils(add,True,unit=Id)
    client.close()

def writeCoilFalse(Id,add):
    client.connect()
    rcl=client.write_coils(add,True,unit=Id)
    client.close()

def gen_writeCoilSeq(Cmps,Mafs,V): # compartments,Manifolds,Valvespermanifolds
    IDseq=[]
    fin=[]
    maniSeq=[]
    for i in range (len(V)):
        print (V[i])
        for j in range (len(V[i])):
            temp=[]
            k=0
            for h in range (0,V[i][j]):
                k=k+1
                temp.append(k)
            IDseq.append(temp)
    print (IDseq)
    l=max(IDseq,key=len)
    print (l)
    for i in range (len(l)):
        for j in range (len(IDseq)):
            try:
                print (IDseq[j][i])
                fin.append(IDseq[j][i])
                print ("J  :"+str(j+1))
                maniSeq.append(j+1)
            except IndexError:
                print ('DoNothing')
    print ("+++++++++++++++++++++++++++++++")
    return fin,maniSeq

def get_startStatus():
    return int(redis.get('st'))


def initializePurge(Valve,Manifold,MinPres):
    print (Valve)
    print (Manifold)
    for i in range (len(Manifold)):
            if(getpressureData()>MinPres and get_startStatus()==1):
                print ("purging manifold"+str(Manifold[i])+"---valve"+str(Valve[i]))
                #writeCoilTrue(Manifold[i],Valve[j])
                time.sleep(4)
                #writeCoilFalse(i,j)

maxThreshold=20     ###
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
    compartments=convert_Toint(compartments)
    manifolds=convert_Toint(manifolds)
    vPmf=convertArr_Toint(vPmf)
    maxThreshold=int(maxThreshold[0])
    minThreshold=int(minThreshold[0])
    print ("MMMMMMTTTTTTTTT   "+str(maxThreshold))
    print ("mmmmmmttttttttttt   "+str(minThreshold))
    IDarray,ManifoldOrd=gen_writeCoilSeq(compartments,manifolds,vPmf)
    print (IDarray)
    print (ManifoldOrd)
    while True:
        #start=int(redis.get('st'))
        pressure=getpressureData()
        print (' Normal Operation pressure  :' + str(pressure)+" ; maxT  :"+str(maxThreshold))
        while(get_startStatus()==1):
            if( getpressureData() >= maxThreshold):
                    print ('initializing purging sequence')
                    initializePurge(IDarray,ManifoldOrd,minThreshold)
            else:
                print ('Scanning pressure pressure normal')
            time.sleep(2)
        time.sleep(2)
                       
except KeyboardInterrupt:
    client.close()


    
