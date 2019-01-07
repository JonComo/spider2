#!/usr/bin/env python
import numpy as np
import socket
from socket import SOL_SOCKET, SO_REUSEADDR
from time import sleep

# sensor
from mpu6050 import mpu6050
sensor = mpu6050(0x68)

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

def set_angles(d):
    for i in range(8):
        angle = float(d[i]) * 2000 + 6000 # angle between -1 and 1
        if angle > 8000:
            angle = 8000
        if angle < 2000:
            angle = 2000
        servo.setTarget(i, int(angle))

def collect_data():
    x = 0
    y = 0
    z = 0
    for i in range(10):
        data = sensor.get_accel_data()
        x += data['x']
        y += data['y']
        z += data['z']
        sleep(.1)

    return "{},{},{}".format(x, y, z)

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
                    
                    if msg == 0:
                        set_angles(d) # just set
                    elif msg == 1:
                        set_angles(d)
                        data = collect_data()
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