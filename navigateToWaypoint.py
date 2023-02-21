import math
import time
import numpy as np
import random
import brickpi3
from Zhengfangxing import go, rot
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

map_size = 210
canvas_size = 768
displacement = 0.05*map_size
scale = canvas_size/(map_size+2 * displacement)
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
particles += [0+displacement*scale, (map_size + displacement)*scale, 0, 1/total_particles]
robot_position = [(84+displacement)*scale, (map_size+displacement-30)*scale, 0]

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
    # rot(-beta * 180 / math.pi, 30)
    for particle in particles:
        current_g_sigma = g_sigma * (alpha / (-math.pi/2))
        g = random.gauss(0, current_g_sigma)
        particle[2] += beta + g
        measures = []
        while True:
            try:
                v = BP.get_sensor(BP.PORT_1)
                print(v)                         # print the distance in CM
                measures.append(v)
                if len(measures) == 10:
                    print(measures)
                    break
            except brickpi3.SensorError as error:
                print(error)
            time.sleep(0.1)
        z = np.median(measures) + sonar_positioin_offset
        prob = calculate_likelihood(particle[0]/scale - displacement,
                                    map_size+displacement - particle[1]/scale,
                                    particle[2],
                                    z)
                                    

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
    print(candidate_m)
    target_index = np.argmin(candidate_m)
    target_wall = candidate_walls[target_index]
    print(target_wall)
    target_m = candidate_m[target_index]
    probability = math.e ** (-(z - target_m)**2 / (2*std_sensor**2)) + K
    return probability


x = (180 + displacement) * scale
y = (map_size + displacement - 30) * scale

navigateToWaypoint(x,y)