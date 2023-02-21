import math
import time
import numpy as np
import random
import brickpi3
BP = brickpi3.BrickPi3()


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
robot_position = [84*scale+displacement*scale, 40*scale+displacement*scale - 30*scale, 0]

print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 40*scale+10*scale, 0+displacement*scale)))
print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))

print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 40*scale+(displacement+5)*scale)))
print ("drawLine:" + str((-5*scale+displacement*scale, 30*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, -5*scale+displacement*scale, 30*scale+(displacement+5)*scale)))
print ("drawLine:" + str((5*scale+10*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

def navigateToWaypoint(X, Y):
    num = 0
    for i in range(10):
        BP.reset_all()
        BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
        try:
            v = BP.get_sensor(BP.PORT_1)
            print(v)                         # print the distance in CM
        except brickpi3.SensorError as error:
            print(error)
        time.sleep(0.1)
        num += 1

navigateToWaypoint(11,1)