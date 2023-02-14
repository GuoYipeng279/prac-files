import math
import time
import numpy as np
import random
from Zhengfangxing import go, rot

scale = 10
displacement = 10
e_sigma = 1 * scale
f_sigma = 0.01
g_sigma = 0.01
d = 10*scale
total_particles = 100.0

sum_rotate = 0.

particles = np.zeros([100, 4])

particles += [0+displacement*scale, 40*scale+displacement*scale, 0, 1/total_particles]

robot_position = [0+displacement*scale, 40*scale+displacement*scale, 0]

# print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 40*scale+10*scale, 0+displacement*scale)))
# print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
# print ("drawLine:" + str((40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale, 40*scale+displacement*scale)))
# print ("drawLine:" + str((40*scale+displacement*scale, 40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))

# print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 40*scale+(displacement+5)*scale)))
# print ("drawLine:" + str((-5*scale+displacement*scale, 30*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

# print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, -5*scale+displacement*scale, 30*scale+(displacement+5)*scale)))
# print ("drawLine:" + str((5*scale+10*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))



def navigation():
    while True:
        Wx = input("input the target x coordinate: ")
        Wy = input("input the target y coordinate: ")
        Wx = Wx*scale + displacement*scale
        Wy = 40*scale + displacement*scale - Wy * scale
        navigateToWaypoint(Wx, Wy)

def navigateToWaypoint(X, Y):
    print(X, Y)
    global robot_position
    # Y - robot_position[1] -> robot_position[1] - Y
    dx, dy = X - robot_position[0], robot_position[1] - Y
    print(dx, dy)
    distance = math.sqrt(dx**2 + dy**2)
    alpha = -math.atan2(dy, dx)
    beta = alpha - robot_position[2]
    print(beta * 180 / math.pi)
    rot(-beta * 180 / math.pi, 3)
    particle_list = []
    for particle in particles:
        # scale g_sigma according to alpha and (-math.pi/2)
        current_g_sigma = g_sigma * (alpha / (-math.pi/2))
        g = random.gauss(0, current_g_sigma)

        particle[2] += alpha + g
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
    # print ("drawParticles:" + str(tuple(particle_list)))
    degree = 0 
    for particle in particles:
        degree += particle[2] * particle[3]
    robot_position[2] = degree

    time.sleep(3)
    go(distance/scale, 3)
    particle_list = []
    for particle in particles:
        # same as g_sigma
        current_e_sigma = e_sigma * (distance / (10*scale))
        current_f_sigma = f_sigma * (distance / (10*scale))
        e = random.gauss(0, current_e_sigma)
        f = random.gauss(0, current_f_sigma)
        # d -> distance
        particle[0] += (distance+e)*math.cos(particle[2])
        print(particle[0])
        particle[1] += (distance+e)*math.sin(particle[2])
        particle[2] += f
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
    # print ("drawParticles:" + str(tuple(particle_list)))
    time.sleep(3)
    sum_x, sum_y, sum_deg = 0, 0, 0
    for particle in particles:
        sum_x += particle[0] * particle[3]
        sum_y += particle[1] * particle[3]
        sum_deg += particle[2] * particle[3]
    robot_position = [sum_x - displacement*scale, sum_y, sum_deg]
    print(robot_position)

navigation()