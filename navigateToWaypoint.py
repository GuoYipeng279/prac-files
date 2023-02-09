import math
import time
import numpy as np
import random
from Zhengfangxing import go, rot

scale = 10
displacement = 10
e_sigma = 1 * scale
f_sigma = 0.01
g_sigma = 0
d = 10*scale
total_particles = 100

particles = np.zeros([100, 4])

particles += [0+displacement*scale, 40*scale+displacement*scale, 0, 1/total_particles]

robot_position = [0+displacement*scale, 40*scale+displacement*scale, 0]

print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 40*scale+10*scale, 0+displacement*scale)))
print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))

print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 40*scale+(displacement+5)*scale)))
print ("drawLine:" + str((-5*scale+displacement*scale, 30*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, -5*scale+displacement*scale, 30*scale+(displacement+5)*scale)))
print ("drawLine:" + str((5*scale+10*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))



def navigation():
    while True:
        Wx = input("input the target x coordinate: ")
        Wy = input("input the target y coordinate")
        Wx = Wx*scale + displacement*scale
        Wy = 40*scale + displacement*scale - Wy * scale
        navigateToWaypoint(Wx, Wy)

def navigateToWaypoint(X, Y):
    dx, dy = X - robot_position[0], Y - robot_position[1]
    distance = math.sqrt(dx**2 + dy**2)
    alpha = math.atan2(dy / dx)
    beta = alpha - robot_position[2]
    rot(beta, 3)
    particle_list = []
    for particle in particles:
        g = random.gauss(0, g_sigma)

        particle[2] += alpha + g
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
    print ("drawParticles:" + str(tuple(particle_list)))
    degree = 0 
    for particle in particles:
        degree += particle[2] * particle[3]
    robot_position[2] = degree

    time.sleep(3)
    go(distance, 3)
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
    time.sleep(3)
    sum_x, sum_y, sum_deg = 0, 0
    for particle in particles:
        sum_x += particle[0] * particle[3]
        sum_y += particle[1] * particle[3]
        sum_deg += particle[2] * particle[3]
    robot_position = [sum_x, sum_y, sum_deg]
    print(robot_position[0]/scale - displacement,
        40+displacement - robot_position[1]/scale,
        robot_position[2])

