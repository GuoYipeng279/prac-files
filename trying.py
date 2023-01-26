import brickpi3
import time 

BP = brickpi3.BrickPi3()

try:
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D)) # reset encoder A
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder D
except IOError as error:
    print(error)

while True:
    BP.set_motor_position(BP.PORT_B,-800)
    BP.set_motor_position(BP.PORT_D,-800)
    BP.set_motor_dps(BP.PORT_B,-100)
    BP.set_motor_dps(BP.PORT_D,-100)
    '''
        B=BP.get_motor_encoder(BP.PORT_B)
        D=BP.get_motor_encoder(BP.PORT_D)
        print('B position: ',B,'D position: ',D)'''
    if KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()
    else:
        pass
