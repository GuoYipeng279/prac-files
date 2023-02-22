from __future__ import print_function
from __future__ import division
import math
import time
import numpy as np
import random
import brickpi3
from Zhengfangxing import go, rot
from particleDataStructures import Map, Canvas

BP = brickpi3.BrickPi3()

BP.reset_all()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
# try:
#     while True:
#         # read and display the sensor value
#         # BP.get_sensor retrieves a sensor value.
#         # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
#         # BP.get_sensor returns the sensor value (what we want to display).
#         try:
#             value = BP.get_sensor(BP.PORT_1)
#             print(value)                         # print the distance in CM
#         except brickpi3.SensorError as error:
#             print(error)
        
#         time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

# except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
#     BP.reset_all()


e_sigma = 1 
f_sigma = 0.01
g_sigma = 0.01
d = 10
total_particles = 100

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
particles += [84, 30, 0, 1/total_particles]
robot_position = [84, 30, 0]

my_canvas = Canvas()

def navigateToWaypoint(X, Y):
    global robot_position
    global particles
    # print(X, Y)
    # print(robot_position[0], robot_position[1])
    sonar_positioin_offset = 1
    dx, dy = X - robot_position[0], robot_position[1] - Y
    # print("dx: ", dx, "dy: ", dy)
    distance = math.sqrt(dx**2 + dy**2)
    alpha = -math.atan2(dy, dx)
    beta = alpha - robot_position[2]
    # print(beta * 180 / math.pi)
    if beta != 0:
        rot(-beta * 180 / math.pi, 30)
        # BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
        measures = []
        while True:
            try:
                v = BP.get_sensor(BP.PORT_1)
                # print(v)                         # print the distance in CM
                measures.append(v)
                if len(measures) == 10:
                    # print(measures)
                    break
            except brickpi3.SensorError as error:
                print(error)
            time.sleep(0.01)
            z = np.median(measures) + sonar_positioin_offset
        for particle in particles:
            current_g_sigma = g_sigma * (alpha / (-math.pi/2))
            g = random.gauss(0, current_g_sigma)
            particle[2] += beta + g
            sonar_positioin_offset = 0
            prob = calculate_likelihood(particle[0], particle[1], particle[2], z)
            particle[3] *= prob

        # normalize
        particles[:, 3] = particles[:, 3] / np.sum(particles[:, 3])

        degree = 0
        for particle in particles:
            degree += particle[2] * particle[3]
        robot_position[2] = degree
        my_canvas.drawParticles(particles)
        particles = resampling(particles)

    time.sleep(2)
    while distance > 0:
        if distance > 20:
            go(20, 10)
            distance -= 20
            distance_moved = 20
        else:
            go(distance, 10)
            distance_moved = distance

        measures = []
        while True:
            try:
                v = BP.get_sensor(BP.PORT_1)
                print(v)                         # print the distance in CM
                measures.append(v)
                if len(measures) > 10:
                    break
            except brickpi3.SensorError as error:
                print(error)
            time.sleep(0.02)
            z = np.median(measures) + sonar_positioin_offset
            
        for particle in particles:
            current_e_sigma = e_sigma * (distance / (distance_moved))
            current_f_sigma = f_sigma * (distance / (distance_moved))
            e = random.gauss(0, current_e_sigma)
            f = random.gauss(0, current_f_sigma)
            # particle[0] += (distance_moved+e)*math.cos(particle[2])
            # particle[1] += (distance_moved+e)*math.sin(particle[2])
            particle[2] += f
            
            prob = calculate_likelihood(particle[0], 
                                        particle[1], 
                                        particle[2],
                                        z)
            # print(prob, end='')
            particle[3] *= prob
        print(particles[:, 3])
        particles[:, 3] = particles[:, 3] / np.sum(particles[:, 3])
        time.sleep(3)
        my_canvas.drawParticles(particles)

    sum_x, sum_y, sum_deg = 0, 0, 0
    for particle in particles:
        sum_x += particle[0] * particle[3]
        sum_y += particle[1] * particle[3]
        sum_deg += particle[2] * particle[3]
    robot_position = [sum_x, sum_y, sum_deg]
    print(robot_position)
    # particles = resampling(particles)

def calculate_likelihood(x, y, theta, z):
    std_sensor = 1
    K = 0
    candidate_walls = []
    candidate_m = []
    for wall in walls:
        p1 = wall[0]
        p2 = wall[1]
        # print((p2[1]-p1[1])*math.cos(theta) - (p2[0]-p1[0])*math.sin(theta))
        if abs((p2[1]-p1[1])*math.cos(theta) - (p2[0]-p1[0])*math.sin(theta)) > 1e-4:
            m = ((p2[1]-p1[1]) * (p1[0]-x) - (p2[0]-p1[0])*(p1[1]-y)) /  \
                ((p2[1]-p1[1])*math.cos(theta) - (p2[0]-p1[0])*math.sin(theta))
            print('m:',m,' theta:',theta,' x:',x,' y:',y)
            print("min x: ", min(p1[0], p2[0]))
            print("max x: ", max(p1[0], p2[0]))
            print(x + m * math.cos(theta))
            print("min y: ", min(p1[1], p2[1]))
            print("max y: ", max(p1[1], p2[1]))
            print(y + m * math.sin(theta))
            if m > 0 and min(p1[0], p2[0]) <= x + m * math.cos(theta) <= max(p1[0], p2[0]) and \
                min(p1[1], p2[1]) <= y + m * math.sin(theta) <= max(p1[1], p2[1]):
                candidate_walls.append(wall)
                candidate_m.append(m)
    if len(candidate_walls) > 0:
        target_index = np.argmin(candidate_m)
        # target_wall = candidate_walls[target_index]
        # print(target_wall)
        target_m = candidate_m[target_index]
        probability = math.e ** (-(z - target_m)**2 / (2*std_sensor**2)) + K
    else:
        probability = 0
    return probability

def resampling(old_particles):
    global total_particles
    cumulative_weight =  np.zeros([total_particles])
    new_particles = np.zeros([total_particles, 4])
    for i in range(total_particles):
        weight = old_particles[i][3]
        cumulative_weight[i] = weight + cumulative_weight[-1]
    for i in range(total_particles):
        p = np.random.random()
        for j in range(total_particles):
            if j == 0:
                if p <= cumulative_weight[j]:
                    new_particles[i] = old_particles[j]
            else:
                if cumulative_weight[j-1] < p <= cumulative_weight[j]:
                    new_particles[i] = old_particles[j]
    new_particles[:,3] = 1/total_particles
    return new_particles


my_canvas.drawParticles(particles)
aims = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]
for aim in aims:
    try:
        x = aim[0]
        y = aim[1]
        navigateToWaypoint(x,y)
    except KeyboardInterrupt:  # except the program gets interrupted by Ctrl+C on the keyboard.
            BP.reset_all()