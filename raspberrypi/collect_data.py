from mpu6050 import mpu6050
import maestro
from time import sleep
import numpy as np

sensor = mpu6050(0x68)
servo = maestro.Controller()

for i in range(8):
    servo.setAccel(i, 30)
    servo.setTarget(i, 6000)

def move_to(state):
    for i in range(8):
        servo.setTarget(i, int(state[i]*2000.0) + 6000)
    avg_iters = 15
    accel = np.zeros(3)
    for i in range(avg_iters):
        data = sensor.get_accel_data()
        accel[0] += data['x']
        accel[1] += data['y']
        accel[2] += data['z']
        sleep(.05)
    return accel / float(avg_iters)

sars = []

# start in default
state = np.zeros(8)
move_to(state)

best_y = 0
best_move = np.zeros(8)

i = 0
while True:
    i += 1
    if i % 5 == 0:
        print("doing best move 4x")
        for j in range(4):
            move_to(state)
            move_to(best_move)

    move_to(state)
    state2 = np.random.random(8) * 2 - 1 # state between -1 and 1
    accel = move_to(state2)
    print(accel)
    if accel[1] > best_y:
        print("new best ", accel[1])
        best_y = accel[1]
        best_move = state2.copy()
