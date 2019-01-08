#!/usr/bin/env python
import numpy as np
import socket
from socket import SOL_SOCKET, SO_REUSEADDR
from time import sleep
from utilities import Body

body = Body()
body.default_accel()

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
                    msg = float(d[0])
                    d = d[1:]
                    if msg == 0:
                        body.set_angles(d) # just set
                    elif msg == 1:
                        body.set_angles(d)
                        data = body.collect_data()
                        data = "{},{},{}".format(data[0], data[1], data[2])
                        print("collected: ", data)
                        connection.send(data.encode())
                except Exception as e:
                    print("error: ", e)
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()