from deal_serial import *
import sys
from ctypes import *  
import pwm
import math
import socket
import atexit
import threading
import time


def convert(a):
    i = 0
    for numc in range(0,4):
        i += a[numc] << numc*8
    cp = pointer(c_int(i))
    fp = cast(cp,POINTER(c_float))
    return fp.contents.value
       

def joint(a,n):
    ac = a
    b = 0
    for num in range(0,n):
        ac[num] = ac[num] << (num)*8
        b += ac[num]
    return b

import pipes

def read_pipe(pipefile):

    fpr = open(pipefile, 'r')
    data = fpr.read()
    fpr.close()

    return data


def reset_pipe(pipefile):

    t = pipes.Template()
    t.open(pipefile, 'w')
    t.reset()


def write_pipe(data, pipefile):

    t = pipes.Template()
    fpw = t.open(pipefile, 'w')
    fpw.write(data)
    fpw.close()


def TCPClient():

    global alarm_flag
    write_pipe('abnormal', 'pipe_mmwave_up2')
    data = read_pipe('pipe_up2_mmwave')
    while data == '':
        data = read_pipe('pipe_up2_mmwave')
        time.sleep(0.01)

    if data in ['OK','tumble']:
        reset_pipe('pipe_up2_mmwave')
        print(data)
        time.sleep(2)
        print ('/*******************************/')
        print ('寻找下个目标')
        print ('寻找下个目标')
        print ('寻找下个目标')
        print ('寻找下个目标')
        print ('寻找下个目标')
        print ('寻找下个目标')
        print ('/*******************************/')
        alarm_flag = -2 
        print('alarm_flag',alarm_flag)
# Check if user input the two serial name arguments

def delay_pwmchan():
    global xpfloat,ypfloat,alarm_flag,target_id
    for delay_times in range(0,4):
        if(alarm_flag == -1):
            print('人体x坐标为',xpfloat)        # AX = convert(targets[num3][20:24])
            print('人体y坐标为',ypfloat)        # VX = convert(targets[num3][12:16])      
            pwm.pwm_chan(xpfloat,ypfloat)
            time.sleep(0.5)
        else:
            break
    if(alarm_flag == -1):
        alarm_flag = joint(target_id,4)
        print('alarm_flag',alarm_flag) 
        #time.sleep(0.5)      
        threading.Thread(target=TCPClient).start()  

try:
    GotSerName = 1
    serCom = sys.argv[1]
    serDat = sys.argv[2]
except:
    print('\nError !\n\nPlease add serial port name next to the "mmwave.py",\n\n'
          + 'first for the command port, next is the data port,\n\n'
          + 'like this: python mmwave.py /dev/ttyACM0 /dev/ttyACM1 \n\n')
    GotSerName = 0

        
if GotSerName:
     
    serInsCom = OpenSerial(serCom, 115200, 1)
    serInsDat = OpenSerial(serDat, 921600, 1)
    # Read one byte here
    # oneByte = ReadByteFromSerial(serInsDat)
    # print(oneByte)
    try:
        config = sys.argv[3]
        if config == 'config':
            ConfigMMWave(serInsCom, 'config.cfg')
        print(sys.argv[4])
        if sys.argv[4] == 'close':
            CloseMMWave(serInsCom)
    except:
        pass    

#参数初始化
#global alarm_flag
lostsync = 1
sync = (2,1,4,3,6,5,8,7)
framenum = 0
alarm = 'alarm'.encode()
alarm_flag = -2
pwm.pwm_init()
numtargets = 0
xpfloat = 0
ypfloat = 0
target_id = []


while True: #总匹配帧数
    while lostsync:
        num1 = 0
        for num1 in range(0,8):
            if( ReadIntFromSerial(serInsDat) != sync[num1] ):
                #print('Continuing matching...\n')
                break
        if num1 == 7:
            lostsync = 0
            framenum += 1
            rxheader = [2,1,4,3,6,5,8,7]
            for numread0 in range(0,44):
                rxheader.append(ReadIntFromSerial(serInsDat))
            #print(framenum)
            #print('sync')
            #print(sync)
            #print('rxheade')
            #print(rxheader)
            packetlength = joint(rxheader[20:24],4)
            #print('packetlength is ')
            #print(rxheader[20:24])
            #print(packetlength)
            #print('realframenumber is ')
            realframenumber = joint(rxheader[24:32],8)#从上电后开始帧数
            #print(rxheader[24:32])
            #print(realframenumber)
            numtlvs = joint(rxheader[48:50],2)
            #print('numtlvs is ')
            #print(numtlvs) 
            print('got sync',realframenumber)
    if lostsync == 0:
        numtargets = 0
        if numtlvs < 10000:
            for numread in range(0,numtlvs):
                #获取tlv数据头
                tlvheader = []
                for numread1 in range(0,8):
                    tlvheader.append(ReadIntFromSerial(serInsDat))
                # print('tlvtype is')
                # print(tlvheader[0:4])
                # print('tlvlength is')
                valuelength = joint(tlvheader[4:8],4) - 8
                # print(tlvheader[4:8])
                #print(valuelength)
                if valuelength < 10000:
                    if tlvheader[0:4] == [8,0,0,0]:
                        targetindex = []
                        for numvalueless1 in range(0,valuelength):
                            targetindex.append(ReadIntFromSerial(serInsDat))
                        #print('targetindex is')
                        #print(targetindex)
                    elif tlvheader[0:4] == [6,0,0,0]:
                        point = []
                        for numvalueless2 in range(0,valuelength):
                            point.append(ReadIntFromSerial(serInsDat))
                        #print('point is')
                        #print(point)
                    elif tlvheader[0:4] == [7,0,0,0]:
                        numtargets = int(valuelength / 68) #TARGETS总数
                        #print('targets number is')
                        #print(numtargets)
                        target = []
                        for numvalueless3 in range(0,valuelength):
                            target.append(ReadIntFromSerial(serInsDat))
                        #print('target is')
                        #print(target)
                    else:
                        break
                else:
                    print("不卡不卡就不卡! - value_length")
                    lostsync = 1
        else:
            print("不卡布卡就不卡! - num_tlv")
            lostsync = 1
            
        targets = []
        for num1 in range(0,numtargets):                    #拆分多维list
            targets.append(target[68*num1:(num1+1)*68])
            #print('targets is')
            #print(targets[num1])
        if alarm_flag == -1:                              #第二次检查加速度及速度
            for num3 in range(0,numtargets):              #轮询各个TARGETS
                if(targets[num3][0:4] == target_id):       #找到与第一次相同的target_id
                    xp = targets[num3][4:8]
                    yp = targets[num3][8:12]
                    xpfloat = convert(xp)      # if(targets[num3][0:4] == target_id):       #找到与第一次相同的target_id   
                    ypfloat = convert(yp)          # AY = convert(targets[num3][24:28])
                    break
                if(num3 == numtargets-1):
                    print('/*******************************/')
                    print("第二次检测失败")
                    print("第二次检测失败")
                    print("第二次检测失败")
                    print("第二次检测失败")
                    print("第二次检测失败")
                    print('/*******************************/')
                    alarm_flag = -2
                    print('alarm_flag',alarm_flag)
        elif alarm_flag == -2:                          #有异常物体
            for num2 in range(0,numtargets):             #轮询各个TARGETS
                AX = convert(targets[num2][20:24])
                AY = convert(targets[num2][24:28])
                VX = convert(targets[num2][12:16])
                VY = convert(targets[num2][16:20])
                A_mod = math.sqrt(math.pow(AX,2)+math.pow(AY,2))
                V_mod = math.sqrt(math.pow(VX,2)+math.pow(VY,2)) 
                print('人体加速度为',A_mod)
                print('人体速度为',V_mod)
                if (A_mod > 6.5 and  V_mod > 1):  #初步判断
                    print('/*******************************/')
                    print("初级判断第一次触发")
                    print("初级判断第一次触发")
                    print("初级判断第一次触发")
                    print("初级判断第一次触发")
                    print("初级判断第一次触发")
                    print('/*******************************/')
                    target_id = []
                    target_id = targets[num2][0:4]
                    xp = targets[num2][4:8]
                    yp = targets[num2][8:12]
                    xpfloat = convert(xp)      # if(targets[num3][0:4] == target_id):       #找到与第一次相同的target_id   
                    ypfloat = convert(yp)          # AY = convert(targets[num3][24:28])
                    print('target_id',target_id)
                    alarm_flag = -1
                    print('alarm_flag',alarm_flag)
                    threading.Thread(target=delay_pwmchan).start() 
                    break #判断到第一个物体异常物体结束循环
        else:
            pass
        numtargets = 0
        lostsync = 1
