from serial import *
import numpy as np
from time import sleep

s = Serial("COM5", 4000000)
s.set_buffer_size(rx_size=1000000)

found = False

def start_printing(s):
    data = s.read(10)
    counts = np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]])
    for i in range(39999):
        data = s.read(10)
        counts = counts + np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]])
        # print(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
    
    print(counts)

def GetCounts(s, exp_rate = 40000):
    data = s.read(10)
    counts = np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    for i in range(exp_rate-1):
        data = s.read(10)
        counts = counts + np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    return counts

def FindHeader(s):
    for i in range(10):
        try_head = s.read(1)
        print(try_head[0])
        if try_head[0] == 47:
            print("Header found, ready to proceed.")
            sleep(1)
            return
    print("Header not found. There is some issue with the input channel.")


found = False

while (found == False):    
    pos_head = s.read(1)
    if pos_head[0] == 47:
        print('Head found')
        found = True
        print(GetCounts(s))
        for i in range(50):
            print(GetCounts(s))
            sleep(0.1)

s.close()