import socket
import threading        

def tcp_client():

    global alarm_flag
    sockIns = socket.create_connection(("127.0.0.1", 12345))
      
    sockIns.send('mmwave_true'.encode())

    # Blocking
    sockIns.recv(1024)
        
    alarm_flag = -1
    sockIns.close()

        
if __name__ == '__main__':

    global alarm_flag
    alarm_flag = 1

    tcp_client()
    print(alarm_flag)



