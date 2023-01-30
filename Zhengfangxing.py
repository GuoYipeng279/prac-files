import brickpi3
import time 
import math

BP = brickpi3.BrickPi3()

r = 5
def go_straight(v):
    global r
    dps = v / (r*math.pi) * 360
    BP.set_motor_dps(BP.PORT_B, dps)
    BP.set_motor_dps(BP.PORT_D, dps)

def rotate(dps):
    BP.set_motor_dps(BP.set_motor_dps(BP.PORT_B, dps))
    BP.set_motor_dps(BP.set_motor_dps(BP.PORT_D, -dps))

# try:
#     BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder D
# except IOError as error:
#     print(error)

# try:
#     start = time.time()
#     while True:
#         v = 10
#         time_need = 40/v
#         go_straight(v)
#         if time.time() - start >= time_need:
#             break
#         time.sleep(0.02)
# except:
#     print('error')

try:
    start = time.time()
    while True:
        v = 10*12/5
        time_need = 90/v
        rotate(v)
        if time.time() - start >= time_need:
            break
        time.sleep(0.02)
except:
    print('error')

# BP.set_motor_position(BP.PORT_B,-800)
# BP.set_motor_position(BP.PORT_D,-800)
# BP.set_motor_dps(BP.PORT_B,-100)
# BP.set_motor_dps(BP.PORT_D,-100)
'''
    B=BP.get_motor_encoder(BP.PORT_B)
    D=BP.get_motor_encoder(BP.PORT_D)
    print('B position: ',B,'D position: ',D)'''
if KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()
else:
    pass
