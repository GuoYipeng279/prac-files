import brickpi3
import time
import math
import keyboard

BP = brickpi3.BrickPi3()

d = 5.3
w = 15.0
s = 1
a = 2
l = 1.02
# l = 1
r = 1


def go_straight(v):
    global d, l, r
    dps = v / (d*math.pi) * 360
    return -dps * l , -dps * r
    dps1 = BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, dps)


def rotate(dps):
    global d, l, r
    ans = dps*w/d
    return ans * 1.2, -ans * r
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

# print('something')
try:
    go(40, 3)
    rot(90, 3)
    go(40, 3)
    rot(90, 3)
    go(40, 3)
    rot(90, 3)
    go(40, 3)
    rot(90, 3)
except:
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    print('error')
    BP.reset_all()

# try:
#     while True:
#         print(1)
#         left, right = 0,0
#         inp = input()
#         print(inp)
#         if inp == w:
#             print(3)
#             left -= 100
#             right -= 100
#         if inp == s:
#             left += 100
#             right += 100
#         if inp == a:
#             left -= 100
#             right += 100
#         if inp == d:
#             left += 100
#             right -= 100
#         print(7)
#         BP.set_motor_dps(BP.PORT_B, left)
#         BP.set_motor_dps(BP.PORT_D, right)
#         time.sleep(0.02)
# except Exception:
#     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
#     print(Exception)
    


# try:
#     go(-40, 3)
# except:
#     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
#     print('error')

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
