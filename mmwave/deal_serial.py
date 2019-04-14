import serial, time

def ConfigMMWave(serIns, filePath):

    # Open config file
    with open('config.cfg', 'r') as cfgFpr:
        cfgStr = cfgFpr.read()

    # Split string by '\n'
    cfgList = cfgStr.split('\n')

    print('\nConfiguring mmWave ...\n')
    for item in cfgList:
        
        # Send '\n' to vaild the command        
        serIns.write(item.encode() + b'\n')

        # First line for command print back
        # Second line shows the command execution result
        # delay for a reasonable mmwave configuration behavior
        time.sleep(0.1)
        replyByte = serIns.readline()
        replyByte += serIns.readline()
        replyStr = replyByte.decode()
        print(replyStr)
    print('\nConfiguration done.\n')

    return serIns


def OpenSerial(comPort, baud, timeout):

    serIns = serial.Serial(comPort, baud, timeout=timeout)

    return serIns
    
def CloseMMWave(serIns):
    
    serIns.write(b'sensorStop\n')
    
    time.sleep(0.1)
    replyByte = serIns.readline()
    replyByte += serIns.readline()
    replyStr = replyByte.decode()
    print(replyStr)
    
    print('mmwave closed.\n')


def ReadIntFromSerial(serIns):

    # Read 1 byte from serial
    replyByte = serIns.read()
    #print(replyByte)
    replyInt = ord(replyByte)
    # replyInt = 1
   
   
    return replyInt
