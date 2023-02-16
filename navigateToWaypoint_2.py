import math
import time
import numpy as np
import random
from Zhengfangxing import go, rot
import brickpi3
BP = brickpi3.BrickPi3()

scale = 10
displacement = 10
e_sigma = 1 * scale
f_sigma = 0.01
g_sigma = 0.01
d = 10*scale
total_particles = 100.0

point_O = (0, 0)
point_A = (0, 168)
point_B = (84, 168)
point_C = (84, 126)
point_D = (84, 210)
point_E = (168, 210)
point_F = (168, 84)
point_G = (210, 84)
point_H = (210, 0)
wall_a = (point_O, point_A)
wall_b = (point_A, point_B)
wall_c = (point_C, point_D)
wall_d = (point_D, point_E)
wall_e = (point_E, point_F)
wall_f = (point_F, point_G)
wall_g = (point_G, point_H)
wall_h = (point_H, point_O)
walls = [wall_a, wall_b, wall_c, wall_d, wall_e, wall_f, wall_g, wall_h]

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

        particle[2] += beta + g
        z = measure
        prob = calculate_likelihood(particle[0]/scale - displacement, 
                                    scale+displacement - particle[1]/scale, 
                                    particle[2],
                                    z)
        particle[3] *= prob
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
        particle[1] += (distance+e)*math.sin(particle[2])
        particle[2] += f
        z = measure
        prob = calculate_likelihood(particle[0]/scale - displacement, 
                                    scale+displacement - particle[1]/scale, 
                                    particle[2],
                                    z)
        particle[3] *= prob
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
    # print ("drawParticles:" + str(tuple(particle_list)))
    time.sleep(3)
    
    sum_x, sum_y, sum_deg = 0, 0, 0
    for particle in particles:
        sum_x += particle[0] * particle[3]
        sum_y += particle[1] * particle[3]
        sum_deg += particle[2] * particle[3]
    robot_position = [sum_x, sum_y, sum_deg]
    print(robot_position)
    print(robot_position[0]/scale - displacement, displacement + 40 - robot_position[1]/scale, robot_position[2])

def calculate_likelihood(x, y, theta, z):
    std_sensor = 1
    K = 0
    candidate_walls = []
    candidate_m = []
    for wall in walls:
        p1 = wall[0]
        p2 = wall[1]
        m = ((p2[1]-p1[1]) * (p1[0]-x) - (p2[0]-p1[0])*(p1[1]-y)) /  \
            ((p2[1]-p1[1])*math.cos(theta) - (p2[0]-p1[0])*math.sin(theta))
        if min(p1[0], p2[0]) < x + m * math.cos(theta) < max(p1[0], p2[0]) and \
            min(p1[1], p2[1]) < y + m * math.sin(theta) < max(p1[1], p2[1]):
            candidate_walls.append(wall)
            candidate_m.append(m)
    target_index = np.argmin(candidate_m)
    target_wall = candidate_walls[target_index]
    target_m = candidate_m[target_index]
    probability = math.e ** (-(z - target_m)**2 / (2*std_sensor**2)) + K
    return probability





BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
navigation()