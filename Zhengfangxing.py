import brickpi3
import time
import math
# import keyboard
import numpy as np
import copy
import random

scale = 10
displacement = 10
e_sigma = 1 * scale
f_sigma = 0.01
g_sigma = 0.01
d = 10*scale
alpha = -math.pi/2

BP = brickpi3.BrickPi3()

diameter = 5.3
w = 20.0
s = 1
a = 2
l = 1
# l = 1
r = 1

total_particles = 100.0

particles = np.zeros([100, 4])

particles += [0+displacement*scale, 40*scale+displacement*scale, 0, 1/total_particles]

def go_straight(v):
    global diameter, l, r
    dps = v / (diameter*math.pi) * 360
    return -dps * 1.05 , -dps * r
    dps1 = BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, dps)


def rotate(dps):
    global diameter, l, r
    ans = dps*w/diameter
    return ans , -ans * 1.2
    BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, -dps)

# try:
#     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder D
# except IOError as error:
#     print(error)


def go(distance, speed=10):
    start = time.time()
    while True:
        timing = distance/speed
        dps1, dps2 = go_straight(speed)
        BP.set_motor_dps(BP.PORT_B, dps1)
        BP.set_motor_dps(BP.PORT_D, dps2)
        if time.time() - start >= timing:
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.reset_all()
            break
        time.sleep(0.02)


def rot(degree, velocity=30):
    start = time.time()
    while True:
        timing = degree/velocity
        dps1, dps2 = rotate(velocity)
        BP.set_motor_dps(BP.PORT_B, dps1)
        BP.set_motor_dps(BP.PORT_D, dps2)
        if time.time() - start >= timing:
            BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
            BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
            BP.reset_all()
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

if __name__ == '__main__':
    BP.reset_all()
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    # try:
    #     go(40, 3)
    #     rot(90, 3)
    #     go(40, 3)
    #     rot(90, 3)
    #     go(40, 3)
    #     rot(90, 3)
    #     go(40, 3)
    #     rot(90, 3)
    # except:
    #     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
    #     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    #     print('error')
    #     BP.reset_all()

    try:
        
        print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 40*scale+10*scale, 0+displacement*scale)))
        print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
        print ("drawLine:" + str((40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale, 40*scale+displacement*scale)))
        print ("drawLine:" + str((40*scale+displacement*scale, 40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
        
        print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 40*scale+(displacement+5)*scale)))
        print ("drawLine:" + str((-5*scale+displacement*scale, 30*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

        print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, -5*scale+displacement*scale, 30*scale+(displacement+5)*scale)))
        print ("drawLine:" + str((5*scale+10*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

        
        for i in range(4):
            for j in range(4):
                go(10, 10)
                particle_list = []
                for particle in particles:
                    e = random.gauss(0, e_sigma)
                    f = random.gauss(0, f_sigma)
                
                    particle[0] += (d+e)*math.cos(particle[2])
                    particle[1] += (d+e)*math.sin(particle[2])
                    particle[2] += f
                    particle_tuple = (particle[0], particle[1], particle[2])
                    particle_list.append(particle_tuple)
        
                print ("drawParticles:" + str(tuple(particle_list)))
                time.sleep(2.5)
            rot(90, 3)
            particle_list = []
            for particle in particles:
                g = random.gauss(0, g_sigma)
                particle[2] += alpha + g
                particle_tuple = (particle[0], particle[1], particle[2])
                particle_list.append(particle_tuple)
        
            print ("drawParticles:" + str(tuple(particle_list)))
            time.sleep(2.5)

    except:
        BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
        print('error')
        BP.reset_all()
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
    # if KeyboardInterrupt:  # except the program gets interrupted by Ctrl+C on the keyboard.
    #     BP.reset_all()
    # else:
    #     pass
