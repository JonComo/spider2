from spider import Body

body = Body()

while True:
    body.update()

    print(body.fast_accel()[1])
