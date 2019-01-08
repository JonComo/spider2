# sensor
from mpu6050 import mpu6050

# servo
# min 4000, mid 6000, max 8000
import maestro

from time import sleep

class Body(object):
    def __init__(self):
        self.servo = maestro.Controller()
        self.sensor = mpu6050(0x68)

        self.x_fast = 0
        self.y_fast = 0
        self.z_fast = 0

        self.x_slow = 0
        self.y_slow = 0
        self.z_slow = 0

    def update(self):
        data = self.sensor.get_accel_data()
        
        self.x_fast += (data['x'] - self.x_fast) * .8
        self.y_fast += (data['y'] - self.y_fast) * .8
        self.z_fast += (data['z'] - self.z_fast) * .8

        self.x_slow += (data['x'] - self.x_slow) * .1
        self.y_slow += (data['y'] - self.y_slow) * .1
        self.z_slow += (data['z'] - self.z_slow) * .1

    def fast_accel(self):
        x_diff = self.x_fast - self.x_slow
        y_diff = self.y_fast - self.y_slow
        z_diff = self.z_fast - self.z_slow
        
        return [x_diff, y_diff, z_diff]

    def set_angles(self, d):
        for i in range(8):
            angle = float(d[i]) * 2000 + 6000 # angle between -1 and 1
            if angle > 7500:
                angle = 7500
            if angle < 2500:
                angle = 2500
            self.servo.setTarget(i, int(angle))

    def default_accel(self):
        for i in range(8):
            self.servo.setAccel(i, 30)
            self.servo.setTarget(i, 6000)

    def collect_data(self, steps=10, sleep_time=.1):
        x = 0
        y = 0
        z = 0

        for i in range(steps):
            data = self.sensor.get_accel_data()
            x += data['x']
            y += data['y']
            z += data['z']
            sleep(sleep_time)

        return [x, y, z]