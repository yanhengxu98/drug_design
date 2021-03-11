import numpy as np
import zerorpc
import time
import numpy
from PIL import Image
import serial
import random
import matplotlib.pyplot as plt


# yj_auto = zerorpc.Client(timeout=20000, heartbeat=50)
# yj_auto.connect("tcp://127.0.0.1:4245")
pump = zerorpc.Client(timeout=20000, heartbeat=50)
pump.connect("tcp://127.0.0.1:4242")
angle = serial.Serial("com8", 9600)

pump. set_temporary_speed(1, 200)
pump. set_temporary_speed(3, 200)
pump. set_temporary_speed(4, 200)
a=pump.get_current_position(1)
b=pump.get_current_position(3)
c=pump.get_current_position(4)

time.sleep(2)
angle.write(b'26')
time.sleep(2)
pump.set_valve(1, 1)
time.sleep(0.5)
pump.suck(1, (12000-a)/12000)
pump.suck(3, 20*(9600-b)/9600)
pump.suck(4, 5*(12000-c)/12000)
time.sleep(10)
pump.set_valve(1, 2)
time.sleep(1)
angle.write(b'27')
time.sleep(1)

def feedback(i, j, k):
    pump.discharge(1,i)
    pump.discharge(3, j)
    pump.discharge(4, k)
    time.sleep(10)
    print( pump.get_current_position(1),  pump.get_current_position(3) , pump.get_current_position(4))
    if pump.get_current_position(1) <= 2400:
        pump.set_valve(1, 1)
        time.sleep(0.5)
        pump.suck(1, (12000 - pump.get_current_position(1)) / 12000)
        pump.set_valve(1, 2)
    if pump.get_current_position(3)<=2400:
        time.sleep(2)
        angle.write(b'26')
        time.sleep(2)
        pump.suck(3, 20*(9600-pump.get_current_position(3))/9600)
        time.sleep(10)
        angle.write(b'27')
        time.sleep(1)
    if pump.get_current_position(4)<=2400:
        time.sleep(2)
        angle.write(b'26')
        time.sleep(2)
        pump.suck(4, 20 * (9600 - pump.get_current_position(4)) / 9600)
        time.sleep(10)
        angle.write(b'27')
        time.sleep(1)
    else:
        return


i = float(input("please input discharge volume of pump 1"))
j = float(input("please input discharge volume of pump 3"))
k = float(input("please input discharge volume of pump 4"))

feedback(i,j,k)