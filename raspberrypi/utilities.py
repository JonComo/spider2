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