from deal_serial import *
import sys 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from multiprocessing import Process, Pool
from PyQt5.QtWidgets import qApp
import pyqtgraph as pg
import mainwindow
import mywindow
import numpy as np
import serial, time
import serial.tools.list_ports
from ctypes import *  
import math
import socket
import atexit
import threading
import subprocess
import signal
import os
import time
import pwm
import mraa



class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()
        #self.show()
    
    def setUI(self):
        self.ui = mywindow.Ui_MyWindow()               
        self.ui.setupUi(self)
        self.setWindowTitle('About Us')
        
        
    def handle_click(self):
        if not self.isVisible():
               self.show()
               print('secondwindow show')
               
                   
class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.initmenu()
        #pwm.pwm_init()           #初始化机械臂
        self.close
        self.show()
       
 
    def TCPRecvPoint(self):
 
            conn, addr = self.sockPoint.accept()
            print('Connected by', addr)          
            while True:
                  xyp = b''
                  xyp = conn.recv(8)
                  while  len(xyp) < 2 :
                         xyp += xyp
                  self.xyp = xyp
                  #print(self.xyp)
                  #self.drawpoint()
                  time.sleep(0.01)
       


    def setUI(self):
        self.ui = mainwindow.Ui_MainWindow()               
        self.ui.setupUi(self)
        self.xyp = b''
        self.xpfloat = 0
        self.ypfloat = 0
        HOST = '127.0.0.1'             
        PORT = 11112
        self.sockPoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockPoint.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockPoint.bind((HOST, PORT))
        self.sockPoint.listen(1)
        #tcpRecvPoint = threading.Thread(target=self.TCPRecvPoint)
        #tcpRecvPoint.start()
        self.setWindowTitle('ICARES') 
        self.ui.graphicsView.setRange(xRange=(-3,3), yRange=(0,6),disableAutoRange=True)
        self.ui.graphicsView.setMouseEnabled(x=False, y=False)
        self.getAvailableSerialPortInfoAndPutOntoUI()
        self.ui.pushButton.clicked.connect(lambda:self.start_C())
        self.ui.pushButton_2.clicked.connect(lambda:self.stop_C())
        self.ui.pushButton_3.clicked.connect(lambda:self.serialstatus())
        self.ui.pushButton_4.clicked.connect(lambda:self.CloseMMWave(self.serInsCom))
        self.ui.pushButton_5.clicked.connect(lambda:self.start_M())
        self.ui.pushButton_6.clicked.connect(lambda:self.stop_M())
        threading.Thread(target=self.sensor_read).start()
       

    def initmenu(self):
        self.ui.actionExit.setShortcut('Ctrl+Q')
        self.ui.actionExit.triggered.connect(qApp.quit)
        
    def start_M(self):

        self.subp_mmwave1 = subprocess.Popen("python3 capture.py",shell = True, cwd = '/home/upsquared/mmwave',preexec_fn = os.setsid)
        #time.sleep(5)
        tcpRecvPoint = threading.Thread(target=self.TCPRecvPoint)
        tcpRecvPoint.start()
        time.sleep(3)
        self.subp_tfpose1 = subprocess.Popen("python3 mmwave_track.py /dev/ttyACM0 /dev/ttyACM1",shell = True, cwd = '/home/upsquared/mmwave',preexec_fn = os.setsid)
        self.ui.label_6.setText('start tracking...')
        self.initSerialPlotTimer_M()

        
    
    def stop_M(self):
        #self.p.daemon = True
        os.killpg(os.getpgid(self.subp_tfpose1.pid), signal.SIGTERM)  # Send the signal to all the process groups
        os.killpg(os.getpgid(self.subp_mmwave1.pid), signal.SIGTERM)  # Send the signal to all the process groups
        self.stop_flag = 1   #now u can open serial and close mmwave
        self.ui.label_6.setText('COM STATUS : Ports are closed')    
    
    def start_C(self):
        self.subp_mmwave = subprocess.Popen("python3 main.py",shell = True, cwd = '/home/upsquared/workspace/tensorflow/tf-pose-estimation/previous_ver/src',preexec_fn = os.setsid)
        time.sleep(5)
        #tcpRecvPoint = threading.Thread(target=self.TCPRecvPoint)
        #tcpRecvPoint.start()
        time.sleep(3)
        self.subp_tfpose = subprocess.Popen("python3 mmwave_817.py /dev/ttyACM0 /dev/ttyACM1",shell = True, cwd = '/home/upsquared/mmwave',preexec_fn = os.setsid)
        self.ui.label_6.setText('start caring...')
        self.showpic()
        self.initSerialPlotTimer_C()
        #self.initSerialPlotTimer_M()
    
    def stop_C(self):
        #self.p.daemon = True
        os.killpg(os.getpgid(self.subp_tfpose.pid), signal.SIGTERM)  # Send the signal to all the process groups
        os.killpg(os.getpgid(self.subp_mmwave.pid), signal.SIGTERM)  # Send the signal to all the process groups
        self.stop_flag = 1   #now u can open serial and close mmwave
        self.ui.label_6.setText('COM STATUS : Ports are closed')
        
    def OpenSerial(self, comPort, baud, timeout):
        serIns = serial.Serial(comPort, baud, timeout=timeout)
        return serIns
        


    def serialstatus(self):

        self.serInsCom = self.OpenSerial(self.ui.comboBox.currentText(), 115200, 1)
    
        self.serInsDat = self.OpenSerial(self.ui.comboBox_2.currentText(), 961200, 1)

        uart = self.serInsCom.name
        
        data = self.serInsDat.name
        
        if self.serInsCom.isOpen():
            if self.serInsDat.isOpen():
                if uart != data:
                
                    self.ui.label_6.setText('COM STATUS : Open Successfully')
                    
                    self.ConfigMMWave(self.serInsCom, 'config.cfg')  #配置毫米波
                    #self.t1 = threading.Thread(target=self.datapacktransimit))
                    #self.p = Process(target=self.datapacktransimit)
                    #self.initSerialPlotTimer()
        
                    print('ok')
         
                else:
                     self.ui.label_6.setText('COM STATUS : Ports NOT Connect')
            


    def getAvailableSerialPortInfoAndPutOntoUI(self):

                self.available_ports = serial.tools.list_ports.comports()        #Get available port info
               
                #for num in range(len(self.available_ports)):
                self.ui.comboBox.addItem(self.available_ports[1].device)
                self.ui.comboBox_2.addItem(self.available_ports[0].device)            #Add port name and description in combo box
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
        
        self.serInsCom.close()
        self.serInsDat.close()
        self.ui.label_6.setText('COM STATUS : Ports are closed')        



    def CloseMMWave(self,serInsCom):
    
        self.serInsCom = self.OpenSerial(self.ui.comboBox.currentText(), 115200, 1)
    
        self.serInsDat = self.OpenSerial(self.ui.comboBox_2.currentText(), 961200, 1)

        uart = self.serInsCom.name
        
        data = self.serInsDat.name
        
        if self.serInsCom.isOpen():
            if self.serInsDat.isOpen():
                if uart != data:
                
                    self.ui.label_6.setText('COM STATUS : Open Successfully')
                    
        self.serInsCom.write(b'sensorStop\n')
    
        time.sleep(0.1)
        replyByte = serInsCom.readline()
        replyByte += serInsCom.readline()
        replyStr = replyByte.decode()
        print(replyStr)
    
        print('mmwave closed.\n')

   
    def convert(self,a):
        i = 0
        for numc in range(0,4):
            i += a[numc] << numc*8
        cp1 = pointer(c_int(i))
        fp1 = cast(cp1,POINTER(c_float))
        return fp1.contents.value

    def showpic(self):
        pixmap = QPixmap('/home/upsquared/workspace/tensorflow/tf-pose-estimation/previous_ver/src/out.jpg')
        self.ui.label_8.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height()) 
        self.show()

    
    def drawpoint(self):
        
        self.ui.graphicsView.clear()
        #x,y = datapacktransimit(self.serInsDat,xpfloat1,ypfloat1)
        r = 0.5
        xp1=self.xyp[0:4]
        yp1=self.xyp[4:8]
        xp=[]
        yp=[]
        for num in range(0,4):
            xp.append(xp1[num])
            #print(xp)
        for num1 in range(0,4):
            yp.append(yp1[num1])
        #print(xp)
        #print(yp)        
        theta = np.arange(0, 2*np.pi, 0.01)
        # for numplot in range(0,self.numtargets):
        x = self.convert(xp) + r * np.cos(theta)
        y = self.convert(yp) + r * np.sin(theta)
            # #self.ui.graphicsView.plot(x0, y0)
        self.ui.graphicsView.plot(x, y)
        #print(' self.xyp is ')
        #print(self.xyp)
        #print(self.convert(xp))
        #print(self.convert(yp))
        #print('-----------------------drawdrawdrawdrawdrawdrawdraw---------------------------')

    
    def initSerialPlotTimer_M(self):

        self.serial_plot_timer = QtCore.QTimer()
        self.serial_plot_timer.timeout.connect(self.drawpoint)
        self.serial_plot_timer.start(1000)
        
    def initSerialPlotTimer_C(self):
         
        self.q_timer = QtCore.QTimer()
        self.q_timer.timeout.connect(self.refresh_img)
        self.q_timer.start(1000)
        
    def refresh_img(self):
      
        self.ui.label_8.setPixmap(QPixmap('/home/upsquared/workspace/tensorflow/tf-pose-estimation/previous_ver/src/img_for_push.png'))


    def sensor_read(self):

        ser_5 = serial.Serial('/dev/ttyS5',115200,timeout=0.5)

        # Read all for a correct format
        ser_5.read(10240)

        # Blocking mode
        ser_5.timeout = None

        while True:
            self.raw_sensor_data = list(ser_5.read(19))
            self.sensor_temper = self.parse_sensor_temper()
            self.sensor_humidity = self.parse_sensor_humidity()
            self.ui.label_2.setText('Temperature :' + self.sensor_temper)
            self.ui.label_3.setText('Humidity :' + self.sensor_humidity)


    def parse_sensor_temper(self):

        sensor_temper = str(self.raw_sensor_data[7]) + str(self.raw_sensor_data[8])

        return sensor_temper

    def parse_sensor_humidity(self):

        sensor_humidity = str(self.raw_sensor_data[11]) + str(self.raw_sensor_data[12]) + str(self.raw_sensor_data[13])

        return sensor_humidity


