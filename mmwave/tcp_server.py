# Echo server program
import socket
import threading
import time


def TCPRecv(sockIns):
    
    global data
    while True:
        conn, addr = sockIns.accept()
        print('Connected by', addr)
        
        with conn:
            data = conn.recv(1024)
            if data.decode() == 'mmwave_true':
                print('MMWave detected person in danger ...')
                time.sleep(6)
                conn.sendall('ok'.encode())


HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
PORT = 12345              # Arbitrary non-privileged port
global data


sockIns =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow reuse
sockIns.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
sockIns.bind((HOST, PORT))
sockIns.listen(1)
    
tcpServThread = threading.Thread(target=TCPRecv, args=(sockIns,))
tcpServThread.start()
