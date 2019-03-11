import sys 
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import mainwindow
import numpy as np
import serial, time
import serial.tools.list_ports
from ctypes import *  
import math
import socket
import atexit
import threading
import time

    
class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.config()
        self.show()
 
 
 
        
    def setUI(self):
        self.ui = mainwindow.Ui_MainWindow()               
        self.ui.setupUi(self)
        self.xpfloat = 0
        self.ypfloat = 0
        self.setWindowTitle('QAQ & OwO') 
        self.ui.graphicsView.setRange(xRange=(-3,3), yRange=(0,6),disableAutoRange=True)
        self.ui.graphicsView.setMouseEnabled(x=False, y=False)
        self.getAvailableSerialPortInfoAndPutOntoUI()
       #self.ui.pushButton.clicked.connect(lambda:self.drawpoint())
        self.ui.pushButton_2.clicked.connect(lambda:self.CloseMMWave(self.serInsCom))
        self.ui.pushButton_3.clicked.connect(lambda:self.serialstatus())
    


    def config(self):
        self.ui.pushButton.clicked.connect(lambda:self.ConfigMMWave(self.serInsCom, 'config.cfg'))
    
    def OpenSerial(self, comPort, baud, timeout):

        serIns = serial.Serial(comPort, baud, timeout=timeout)
        
        return serIns
        


    def serialstatus(self):

        self.serInsCom = self.OpenSerial(self.ui.comboBox.currentText(), 115200, 1)
    
        self.serInsDat = self.OpenSerial(self.ui.comboBox_2.currentText(), 961200, 1)

        if self.serInsCom.isOpen():
            if self.serInsDat.isOpen():
                self.ui.label_6.setText('COM STATUS : Ports Connect Successfully')
                
         
        else:
            self.ui.label_6.setText('COM STATUS : Ports NOT Connect')
            


    def getAvailableSerialPortInfoAndPutOntoUI(self):

                self.available_ports = serial.tools.list_ports.comports()        #Get available port info
               
                for num in range(len(self.available_ports)):
                        self.ui.comboBox.addItem(self.available_ports[num].device)
                        self.ui.comboBox_2.addItem(self.available_ports[num].device)            #Add port name and description in combo box
                        #self.ui.label_16.setText(available_port_description[num])
    


 
    def ConfigMMWave(self, serInsCom, filePath):
        # Open config file
        with open('config.cfg', 'r') as cfgFpr:
            cfgStr = cfgFpr.read()

        # Split string by '\n'
        cfgList = cfgStr.split('\n')

        print('\nConfiguring mmWave ...\n')
        for item in cfgList:
            # Send '\n' to vaild the command        
            self.serInsCom.write(item.encode() + b'\n')

            # First line for command print back
            # Second line shows the command execution result
            # delay for a reasonable mmwave configuration behavior
            time.sleep(0.1)
            replyByte = serInsCom.readline()
            replyByte += serInsCom.readline()
            replyStr = replyByte.decode()
            print(replyStr)

        print('\nConfiguration done.\n')
        self.t1 = threading.Thread(target=self.datapacktransimit,args=(self.serInsDat,))
        self.t1.start()
        self.initSerialPlotTimer()
        



    def CloseMMWave(self,serInsCom):
        self.serInsCom.write(b'sensorStop\n')
    
        time.sleep(0.1)
        replyByte = serInsCom.readline()
        replyByte += serInsCom.readline()
        replyStr = replyByte.decode()
        print(replyStr)
    
        print('mmwave closed.\n')


    def drawpoint(self,xpfloat,ypfloat):
        self.ui.graphicsView.clear()
        #x,y = datapacktransimit(self.serInsDat,xpfloat1,ypfloat1)
        r = 0.05
        theta = np.arange(0, 2*np.pi, 0.01)
        x = self.xpfloat + r * np.cos(theta)
        y = self.ypfloat + r * np.sin(theta)
        #self.ui.graphicsView.plot(x0, y0)
        self.ui.graphicsView.plot(x, y)

    
    def initSerialPlotTimer(self):

        self.serial_plot_timer = QtCore.QTimer()
        self.serial_plot_timer.timeout.connect(lambda:self.drawpoint(self.xpfloat,self.ypfloat))
        self.serial_plot_timer.start(50)
   
                
    def convert(self,a):
        i = 0
        for numc in range(0,4):
            i += a[numc] << numc*8
        cp = pointer(c_int(i))
        fp = cast(cp,POINTER(c_float))
        return fp.contents.value
    

            
    def joint(self,a,n):
        ac = a
        b = 0
        for num in range(0,n):
            ac[num] = ac[num] << (num)*8
            b += ac[num]
        return b
        
        
        
        
    def TCPClient(self):
    
        sockIns = socket.create_connection(("127.0.0.1", 12345)) 
        sockIns.send('mmwave_true'.encode())
        
        while True:
            # Blocking
            data = sockIns.recv(1024)
            if data.decode() in ['OK','a person tumble'] :
                print(data.decode())
                self.alarm_flag = -1
                break
        #self.alarm_flag = -1
        sockIns.close()
        
        
        
    
    def ReadIntFromSerial(self,serInsDat):
    
        # Read 1 byte from serial
        replyByte = self.serInsDat.read()
        replyInt = ord(replyByte)
        # replyInt = 1
        # print(replyByte)
        return replyInt
    
    
    
        
    # def tcplink():
        # global s2,self.alarm_flag
        # s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立连接
        # s2.bind((host, listen_port))        # 绑定端口
        # s2.listen(5)
        # while True:
            # print ('waiting for connection...')
            # sock, addr = s2.accept()
            # print ('Accept new connection from %s:%s...' % addr)
            # while True:
                # data = sock.recv(1024)
                # if data.decode() in ['no person tumble','a person tumble'] :
                # print(data.decode())
                # self.alarm_flag = -1
                # break
            # sock.close()
            # print ('Connection from %s:%s closed.' % addr)
    
    # def close_sock():
        # global s2,s1
        # s1.close()
        # s2.close()
        # print ('closed sock')
    #参数初始化
    def datapacktransimit(self,serInsDat):
        self.alarm_flag = 0
        lostsync = 1
        sync = (2,1,4,3,6,5,8,7)
        xthreshold = 0
        ythreshold = 0
        framenum = 0
        alarm = 'alarm'.encode()
        self.alarm_flag = -1
        host = socket.gethostname() # 获取本地主机名
        alarm_port = 12345                # 设置端口好
        listen_port = 54321
        #t = threading.Thread(target = tcplink,args = ()) 
        #t.start()                                           #开始监听
        #atexit.register(close_sock)#
    
        while True: #总匹配帧数
            while lostsync:
                num1 = 0
                for num1 in range(0,8):
                    if( self.ReadIntFromSerial(self.serInsDat) != sync[num1] ):
                        #print('Continuing matching...\n')
                        break
                if num1 == 7:
                    lostsync = 0
                    framenum += 1
                    rxheader = [2,1,4,3,6,5,8,7]
                    for numread0 in range(0,44):
                        rxheader.append(self.ReadIntFromSerial(self.serInsDat))
                    print('got sync')
                    print(framenum)
                    #print('sync')
                    #print(sync)
                    #print('rxheade')
                    #print(rxheader)
                    packetlength = self.joint(rxheader[20:24],4)
                    #print('packetlength is ')
                    #print(rxheader[20:24])
                    #print(packetlength)
                    #print('realframenumber is ')
                    #realframenumber = joint(rxheader[24:32],8)#从上电后开始帧数
                    #print(rxheader[24:32])
                    #print(realframenumber)
                    numtlvs = self.joint(rxheader[48:50],2)
                    #print('numtlvs is ')
                    #print(numtlvs)
                    
            if lostsync == 0:
                numtargets = 0
                for numread in range(0,numtlvs):
                    #获取tlv数据头
                    tlvheader = []
                    for numread1 in range(0,8):
                        tlvheader.append(self.ReadIntFromSerial(self.serInsDat))
                    # print('tlvtype is')
                    # print(tlvheader[0:4])
                    # print('tlvlength is')
                    valuelength = self.joint(tlvheader[4:8],4) - 8
                    # print(tlvheader[4:8])
                    # print(valuelength)
                    if tlvheader[0:4] == [8,0,0,0]:
                        targetindex = []
                        for numvalueless1 in range(0,valuelength):
                            targetindex.append(self.ReadIntFromSerial(self.serInsDat))
                        #print('targetindex is')
                        #print(targetindex)
                    elif tlvheader[0:4] == [6,0,0,0]:
                        point = []
                        for numvalueless2 in range(0,valuelength):
                            point.append(self.ReadIntFromSerial(self.serInsDat))
                        #print('point is')
                        #print(point)
                    elif tlvheader[0:4] == [7,0,0,0]:
                        numtargets = int(valuelength / 68) #TARGETS总数
                        print('targets number is')
                        print(numtargets)
                        target = []
                        for numvalueless3 in range(0,valuelength):
                            target.append(self.ReadIntFromSerial(self.serInsDat))
                        #print('target is')
                        #print(target)
                    else:
                        break
                
                targets = []
                for num1 in range(0,numtargets):             #拆分多维list
                    targets.append(target[68*num1:(num1+1)*68])
                    #print('targets is')
                    #print(targets[num1])
                print('alarm flag')
                print(self.alarm_flag)
                if self.alarm_flag == -1:                              #未有报警targets
                    for num2 in range(0,numtargets):             #轮询各个TARGETS
                        AX = self.convert(targets[num2][20:24])
                        AY = self.convert(targets[num2][24:28])
                        VX = self.convert(targets[num2][12:16])
                        VY = self.convert(targets[num2][16:20])
                        print('AX is')
                        print(AX)
                        print('AY is')
                        print(AY)
                        print('VX is')
                        print(VX)
                        print('VY is')
                        print(VY)
                        A_mod = math.sqrt(math.pow(AX,2)+math.pow(AY,2))
                        print('A_mod is')
                        print(A_mod)
                        V_mod = math.sqrt(math.pow(VX,2)+math.pow(VY,2))
                        print('V_mod is')
                        print(V_mod)
                        if (A_mod > 0.5 and V_mod < 0.5):  #初步判断
                            target_id = []
                            target_id = targets[num2][0:4]
                            print('target_id is')
                            print(target_id)
                            self.alarm_flag = self.joint(target_id,4)
                            print(self.alarm_flag)
                            xp = targets[num2][4:8]
                            yp = targets[num2][8:12]
                            self.xpfloat = self.convert(xp)  
                            #print(xp)
                            print('self.xpfloat is ')
                            print(self.xpfloat)
                            self.ypfloat = self.convert(yp)  
                            #print(yp)
                            print('self.ypfloat is ')
                            print(self.ypfloat)
                            # s.connect(host, pwm_port)
                            # s.send("xp"+str(self.xpfloat))
                            # s.send("yp"+str(self.xpfloat))
                            # s.close()
                            # s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #建立连接
                            # try:
                                # s1.connect((host, alarm_port))
                                # s1.send(alarm)
                            # except:
                                # print('could not connect')    
                            # s1.close()
                            t = threading.Thread(target=self.TCPClient) 
                            t.start()
                            print ('.....................................')
                            break #判断到第一个物体异常物体结束循环
                else:                          #有异常物体
                    #if numtargets == 0:
                        #self.alarm_flag = -1
                    #else :
                    for num3 in range(0,numtargets):  #获取报警target最新位置
                        if targets[num3][0:4] == target_id:
                            xp = targets[num3][4:8]
                            yp = targets[num3][8:12]
                            self.xpfloat = self.convert(xp)  
                            #print(xp)
                            print('catch id is ')
                            print(target_id)
                            #print('self.xpfloat is ')
                            #print(self.xpfloat)
                            self.ypfloat = self.convert(yp)  
                            #print(yp)
                            #print('self.ypfloat is ')
                            #print(self.ypfloat)
                            break
                            #elif (num3 == numtargets - 1):
                                #self.alarm_flag = -1
                numtargets = 0
                lostsync = 1
                print('one frame read done\n')          
    

