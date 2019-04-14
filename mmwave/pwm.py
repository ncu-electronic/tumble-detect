#!/usr/bin/env python
# Example Usage: Generates PWM at a step rate of 0.01 continuously.

import mraa
import time
import math
import sys

def pwm_init():
    global M1,M2,M3,M4
    # initialise PWM
    M1 = mraa.Pwm(33)
    M2 = mraa.Pwm(32)
    M3 = mraa.Pwm(16)
    # set PWM period
    M1.period_ms(10)
    M2.period_ms(10)
    M3.period_ms(10)
    # enable PWM
    M1.enable(True)
    M2.enable(True)
    M3.enable(True)
    # write PWM value
    M1.write(0.15)
    M2.write(0.22)
    M3.write(0.20)
    M4 = mraa.Gpio(7)
    M4.dir(mraa.DIR_OUT)
    M4.write(0)
    for times in range(0,30):
        M4.write(1)
        time.sleep(0.0012)
        M4.write(0)
        time.sleep(0.0088)
    M4.write(0)
    return 1

        
        
        
def pwm_chan(x,y):
    # initialise PWM
    global M1,M2,M3
    r = math.sqrt(math.pow(x,2)+math.pow(y,2))
    print('r=',r)
    xita = math.atan2(y,x)*180/math.pi
    print('xita=',xita)
    #M1_period = -(1/900.0)*xita+0.25       #0.05-0.27 毫米波天线在上
    M1_period = (1/900.0)*xita+0.05       #0.05-0.27 毫米波天线在下
    #M1_period = x
    #M2_period = y
    #M3_period = z
    if r < 2:
        M2_period = 0.21
        M3_period = 0.19
    elif r < 2.5:
        M2_period = 0.21
        M3_period = 0.20
    elif r < 4:
        M2_period = 0.21
        M3_period = 0.21
    else :
        M2_period = 0.20
        M3_period = 0.21
    #print('M1_period=',M1_period)
    #print('M3_period=',M3_period)
    if (M1_period>0.21):
        M1_period=0.21
    if (M1_period<0.09):
        M1_period = 0.09
    if (M2_period>0.25):
        M2_period=0.25
    if (M2_period<0.18):
        M2_period=0.18
    if (M3_period>0.25):
        M3_period=0.25
    if (M3_period<0.18):
        M3_period=0.18
        # write PWM value
    M1.write(M1_period)
    M2.write(M2_period)
    M3.write(M3_period)
    return 1
    
def pwm_chan_track(x,y):
    # initialise PWM
    global M1,M2,M3
    r = math.sqrt(math.pow(x,2)+math.pow(y,2))
    #print('r=',r)
    xita = math.atan2(y,x)*180/math.pi
    #print('xita=',xita)
    #M1_period = -(1/900.0)*xita+0.25       #0.05-0.27 毫米波天线在上
    M1_period = (1/900.0)*xita+0.05       #0.05-0.27 毫米波天线在下
    #M1_period = 0.15
    #M2_period = x
    #M3_period = y
    if r < 1:
        M2_period = 0.22
        M3_period = 0.21
    elif r < 1.5:
        M2_period = 0.22
        M3_period = 0.22
    elif r < 2.7:
        M2_period = 0.22
        M3_period = 0.23
    elif r < 5:
        M2_period = 0.21
        M3_period = 0.23
    else :
        M2_period = 0.21
        M3_period = 0.24
    #print('M1_period=',M1_period)
    #print('M3_period=',M3_period)
    if (M1_period>0.25):
        M1_period=0.25
    if (M1_period<0.05):
        M1_period = 0.05
    if (M2_period>0.25):
        M2_period=0.25
    if (M2_period<0.10):
        M2_period=0.10
    if (M3_period>0.25):
        M3_period=0.25
    if (M3_period<0.18):
        M3_period=0.18
        # write PWM value
    M1.write(M1_period)
    M2.write(M2_period)
    M3.write(M3_period)
    return 1
if __name__ == "__main__":
    pwm_init()
    pwm_chan(float(sys.argv[1]),float(sys.argv[2]))
    time.sleep(2)
