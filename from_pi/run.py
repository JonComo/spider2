import maestro
from time import sleep
import numpy as np

servo = maestro.Controller()
for i in range(8):
    servo.setAccel(i, 8)
    servo.setTarget(i, 6000)
sleep(3)

while True:
    p = np.random.randint(4000, size=8)
    p += 4000
    for i in range(8):
        servo.setTarget(i, p[i])
    sleep(.5)

while True:
    for i in range(8):
        servo.setTarget(i, 4000)
    sleep(2)

    for i in range(8):
        servo.setTarget(i, 6000)
    sleep(2)

    for i in range(8):
        servo.setTarget(i, 8000)
    sleep(2)

#servo.setSpeed(1,10)     #set speed of servo 1
#x = servo.getPosition(1) #get the current position of servo 1
#servo.close()
