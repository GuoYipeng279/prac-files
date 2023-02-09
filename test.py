import numpy as np
import time
import math
import copy
import random

scale = 10
displacement = 10
e_sigma = 1 * scale
f_sigma = 0.01
g_sigma = 0
d = 10*scale
alpha = -math.pi/2

print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 40*scale+10*scale, 0+displacement*scale)))
print ("drawLine:" + str((0+displacement*scale, 0+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale, 40*scale+displacement*scale)))
print ("drawLine:" + str((40*scale+displacement*scale, 40*scale+displacement*scale, 0+displacement*scale, 40*scale+displacement*scale)))

print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 40*scale+(displacement+5)*scale)))
print ("drawLine:" + str((-5*scale+displacement*scale, 30*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))

print ("drawLine:" + str((-5*scale+displacement*scale, 40*scale+(displacement+5)*scale, -5*scale+displacement*scale, 30*scale+(displacement+5)*scale)))
print ("drawLine:" + str((5*scale+10*scale, 40*scale+(displacement+5)*scale, 5*scale+10*scale, 30*scale+(displacement+5)*scale)))




particles = np.zeros([100, 3])

particles += [0+displacement*scale, 40*scale+displacement*scale, 0]

"""
for particle in particles:
    print ("drawParticles:" + str(tuple(particle)))
"""

for i in range(4):
    for j in range(4):
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
        time.sleep(2)
    particle_list = []
    for particle in particles:
        g = random.gauss(0, g_sigma)

        particle[2] += alpha + g
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
       
    print ("drawParticles:" + str(tuple(particle_list)))
    time.sleep(2)

"""
while True:
    particle_list = []
    for particle in particles: n  
        e = random.gauss(0, e_sigma)
        f = random.gauss(0, f_sigma)
       
        particle[0] += (d+e)*math.cos(particle[2])
        particle[1] += (d+e)*math.sin(particle[2])
        particle[2] += f
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
       
    print ("drawParticles:" + str(tuple(particle_list)))

    time.sleep(2)

while True:
    particle_list = []
    for particle in particles:
        g = random.gauss(0, g_sigma)

        particle[2] += alpha + g
        particle_tuple = (particle[0], particle[1], particle[2])
        particle_list.append(particle_tuple)
       
    print ("drawParticles:" + str(tuple(particle_list)))

    time.sleep(2)
"""