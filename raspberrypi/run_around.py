# Runs around and tries to learn to walk forwards
# Flip robot upsidedown to scramble its brain connections if suck in local optima
# Uses motion sensor to generate rewards for forward motion
# Try using user input

from spider import Body
import numpy as np
from time import sleep

learning_rate = .2
move_steps = 10 # moves to make with trial Ws

body = Body()
body.default_accel()
body.set_angles(np.zeros(8))
sleep(1)

t = 0

def transform(state, W):
    global t
    #state = np.hstack([np.ones(1), state])
    z = W.dot(np.array([1, np.sin(t), np.cos(t)]))
    h = np.tanh(z)
    return h

if __name__ == "__main__":
    W = np.random.randn(8, 3)
    state = np.zeros(8)

    rewards = []
    diffs = []

    i = 0

    while True:
        i += 1

        diff = np.random.randn(W.shape[0], W.shape[1])
        trialW = W + diff
        data = np.zeros(3) # accel data

        for k in range(move_steps):
            t += 0.1
            state = transform(state, trialW)
            body.set_angles(state)
            data += np.array(body.collect_data(steps=10, sleep_time=.01))

        if data[2] < 0:
            # robot is flipped, reset!
            print("resetting")
            i = 0
            rewards = []
            diffs = []
            W = np.random.randn(8, 9)
            state = np.zeros(8)
            body.set_angles(state)
            sleep(5)
            continue
        
        reward = data[1] # y acceleration, maybe want to filter out tilting in y direction?
        user = input()
        if user == 'g':
            reward = 1.0
        else:
            reward = -1.0

        print("reward: ", reward)

        rewards.append(reward)
        diffs.append(diff)

        if i % 5 == 0:
            # train
            print("training")
            state = np.zeros(8)
            body.set_angles(state)

            r_norm = np.array(rewards)
            r_norm -= np.mean(r_norm)
            r_norm /= np.std(r_norm)

            update = np.zeros_like(W)
            for j in range(len(diffs)):
                update += diffs[j] * r_norm[j]
            W += update * learning_rate
            
            rewards = []
            diffs = []