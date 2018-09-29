import os
import time
from threading import Thread

def pro1():
	os.system('sudo python Onmcu.py')
def pro2():
	os.system('sudo python LED.py')
def pro3():
	os.system('AnaIO.py')
def pro4():
	os.system('DigIO.py')
def Main():
	t1=Thread(target=pro1)
	t2=Thread(target=pro2)
	t3=Thread(target=pro3)
	t4=Thread(target=pro4)
	t1.start()
	t2.start()
	t3.start()
	t4.start()

Main()
