from mpu6050 import mpu6050
import maestro
from time import sleep

sensor = mpu6050(0x68)
servo = maestro.Controller()

for i in range(8):
    servo.setAccel(i, 30)
    servo.setTarget(i, 6000)

def move_to(state):
    for i in range(8):
        servo.setTarget(i, int(state[i]*2000 + 6000))
    
    avg_iters = 10
    accel = np.zeros(3)
    for i in range(avg_iters):
        data = sensor.get_accel_data()
        accel[0] += data.x
        accel[1] += data.y
        accel[2] += data.z
    return accel / float(avg_iters)

sars = []

# start in default
state = np.zeros(8)
move_to(state)

while True:
    state2 = np.random.random(8) * 2 - 1 # state between -1 and 1
    accel = move_to(state)
    print(accel)