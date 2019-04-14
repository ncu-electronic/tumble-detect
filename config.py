from deal_serial import *
import sys
from ctypes import *

i = 0
a = 0
serCom = sys.argv[1]
serDat = sys.argv[2]
serInsCom = OpenSerial(serCom, 115200, 1)
serInsDat = OpenSerial(serDat, 921600, 1)
with open("data.txt", "a+") as f:
    while serInsDat.inWaiting() > 0:
        if a == 100:    
            f.close()
            break
        if i == 20:
            f.write("\n")
            a = a + 1
            i = 0
        i = i + 1
        x = ReadIntFromSerial(serInsDat)
        #x = serInsDat.read()
        f.write(str(x)+' ')
