#!/usr/bin/env python
import numpy as np
import socket
from socket import SOL_SOCKET, SO_REUSEADDR
from time import sleep

# servo
# min 4000, mid 6000, max 8000
import maestro
servo = maestro.Controller()

for i in range(8):
    servo.setAccel(i, 30)
    servo.setTarget(i, 6000)

TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 200

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    # wait for a connection
    print ('waiting for a connection')
    connection, client_address = s.accept()

    try:
        # show who connected to us
        print ('connection from', client_address)

        # receive the data in small chunks and print it
        while True:
            data = connection.recv(BUFFER_SIZE)
            if data:
                try:
                    # output received data
                    print ("Data: %s" % data)
                    data = data.decode("utf-8")
                    d = data.split(",")
                    for i in range(8):
                        angle = float(d[i]) * 2000 + 6000 # angle between -1 and 1
                        if angle > 8000:
                            angle = 8000
                        if angle < 2000:
                            angle = 2000
                        servo.setTarget(i, int(angle))
                except:
                    print("error: unknown message")
                    connection.send("error")
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()