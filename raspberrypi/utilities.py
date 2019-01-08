# sensor
from mpu6050 import mpu6050
sensor = mpu6050(0x68)

# servo
# min 4000, mid 6000, max 8000
import maestro
servo = maestro.Controller()

def set_angles(d, servo):
    for i in range(8):
        angle = float(d[i]) * 2000 + 6000 # angle between -1 and 1
        if angle > 8000:
            angle = 8000
        if angle < 2000:
            angle = 2000
        servo.setTarget(i, int(angle))

def default_accel():
    for i in range(8):
        servo.setAccel(i, 30)
        servo.setTarget(i, 6000)

def collect_data(steps=10, sleep_time=.1):
    x = 0
    y = 0
    z = 0

    for i in range(steps):
        data = sensor.get_accel_data()
        x += data['x']
        y += data['y']
        z += data['z']
        sleep(sleep_time)

    return [x, y, z]