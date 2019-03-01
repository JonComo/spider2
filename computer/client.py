#!/usr/bin/env python

import socket
from time import sleep

TCP_IP = 'raspberrypi.local'
TCP_PORT = 5005
BUFFER_SIZE = 1024

class Socket(object):
    def __init__(self):
        self.connect()

    def send(self, msg):
        self.s.sendall(msg.encode())

    def send_recv(self, msg):
        self.s.sendall(msg.encode())
        data = self.s.recv(BUFFER_SIZE)
        return data

    def connect(self):
        print("trying to connect to: ", TCP_IP, TCP_PORT)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))
        print("connected")

    def close(self):
        self.s.close()
        self.s = None
        print("socket closed")

if __name__ == "__main__":
    usr_input = ""
    sock = Socket()

    while usr_input != "q":
        usr_input = input("mssg: ")
        if usr_input == "z":
            for i in range(15):
                sock.send_recv("{},275".format(i))
        else:
            d = sock.send_recv(usr_input)
            print(d)
        

    sock.close()
