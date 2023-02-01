import brickpi3
import time
import math

BP = brickpi3.BrickPi3()

r = 5.5


def go_straight(v):
    global r
    dps = v / (r*math.pi) * 360
    return dps, dps
    dps1 = BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, dps)


def rotate(dps):
    ans = dps*12/5
    return ans, -ans
    BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, -dps)

# try:
#     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder D
# except IOError as error:
#     print(error)


def go(distance, timing):
    start = time.time()
    while True:
        speed = distance/timing
        dps1, dps2 = go_straight(speed)
        BP.set_motor_dps(BP.PORT_B, dps1)
        BP.set_motor_dps(BP.PORT_D, dps2)
        if time.time() - start >= timing:
            break
        time.sleep(0.02)


def rot(degree, timing):
    start = time.time()
    while True:
        velocity = degree/timing
        dps1, dps2 = rotate(velocity)
        BP.set_motor_dps(BP.PORT_B, dps1)
        BP.set_motor_dps(BP.PORT_D, dps2)
        if time.time() - start >= timing:
            break
        time.sleep(0.02)
# jdwio


def curve(distance, degree, timing):
    start = time.time()
    while True:
        speed = distance/timing
        velocity = degree/timing
        dps11, dps12 = go_straight(speed)
        dps21, dps22 = rotate(velocity)
        BP.set_motor_dps(BP.PORT_B, dps11+dps21)
        BP.set_motor_dps(BP.PORT_D, dps12+dps22)
        if time.time() - start >= timing:
            break
        time.sleep(0.02)


try:
    go(43, 3)
    rot(120, 3)
    go(43, 3)
    rot(110, 3)
    go(43, 3)
    rot(116, 3)
    go(43, 3)
    rot(116, 3)
except:
    print('error')

# try:
#     curve(50, 100, 6)
#     curve(50, -100, 6)
#     curve(50, 100, 6)
#     curve(50, -100, 6)
#     curve(50, 100, 6)
#     curve(50, -100, 6)
#     curve(50, 100, 6)
#     curve(50, -100, 6)
# except:
#     print('error')

# BP.set_motor_position(BP.PORT_B,-800)
# BP.set_motor_position(BP.PORT_D,-800)
# BP.set_motor_dps(BP.PORT_B,-100)
# BP.set_motor_dps(BP.PORT_D,-100)
'''
    B=BP.get_motor_encoder(BP.PORT_B)
    D=BP.get_motor_encoder(BP.PORT_D)
    print('B position: ',B,'D position: ',D)'''
if KeyboardInterrupt:  # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()
else:
    pass
