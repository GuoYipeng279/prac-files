import brickpi3
import time
import math
import keyboard
import numpy as np
import copy
import random

scale = 10
displacement = 10
e_sigma = 0.3 * scale
f_sigma = 0.01
g_sigma = 1
d = 10*scale
alpha = 45

BP = brickpi3.BrickPi3()

d = 5.3
w = 15.0
s = 1
a = 2
l = 1
# l = 1
r = 1

print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 40*scale+10*scale, 0+displacement*scale)))
print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))

particles = np.zeros([100, 3])

particles += [0+displacement*scale, 40*scale+displacement*scale, 0]

def go_straight(v):
    global d, l, r
    dps = v / (d*math.pi) * 360
    return -dps * l , -dps * r
    dps1 = BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, dps)


def rotate(dps):
    global d, l, r
    ans = dps*w/d
    return ans * 1, -ans * r *1.05
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
#     for i in range(4):
#         for i in range(4):
#             go(10, 1)
#             particle_list = []
#             for particle in particles:
#                 e = random.gauss(0, e_sigma)
#                 f = random.gauss(0, f_sigma)
            
#                 particle[0] += (d+e)*math.cos(particle[2])
#                 particle[1] += (d+e)*math.sin(particle[2])
#                 particle[2] += f
#                 particle_tuple = (particle[0], particle[1], particle[2])
#                 particle_list.append(particle_tuple)
       
#             # print ("drawParticles:" + str(tuple(particle_list)))
#             time.sleep(5)
#         rot(90, 3)
#         particle_list = []
#         for particle in particles:
#             g = random.gauss(0, g_sigma)
#             particle[2] += 90 + g
#             particle_tuple = (particle[0], particle[1], particle[2])
#             particle_list.append(particle_tuple)
       
#     # print ("drawParticles:" + str(tuple(particle_list)))

#     time.sleep(2)

# except:
#     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
#     print('error')
#     BP.reset_all()

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
