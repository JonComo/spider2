from client import Socket
from time import sleep
import numpy as np

class Spider(object):
    def __init__(self):
        self.s = Socket()
        
    def move(self, angles, msg_type=0, sleep_time=1, accel=30):
        angles = np.round(angles, 2)
        data = "{},{},{},".format(msg_type, sleep_time, accel) + ",".join(map(str, angles))
        if msg_type == 0:
            self.s.send(data)
        else:
            ret_dat = self.s.send_recv(data)
            return list(map(float, ret_dat.decode('utf-8').split(",")))
