from websocket import create_connection
import sys


def SendWebsocket(msg):
    
    ws = create_connection("ws://119.29.136.188:1508/")
    print("Sending ...")
    ws.send(msg)
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received ", result)
    ws.close()
