import brickpi3
import time 

BP = brickpi3.BrickPi3()

try:
    BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) # reset encoder A
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder D
except IOError as error:
    print(error)
    
#BP.set_motor_power(BP.PORT_D, BP.MOTOR_FLOAT)   
    
while True:
                           # float motor D
    #BP.set_motor_limits(BP.PORT_A, 50)                                     # optionally set a power limit
        # The following BP.get_motor_encoder function returns the encoder value
    try:
        target = BP.get_motor_encoder(BP.PORT_D)     # read motor D's position
    except IOError as error:
        print(error)

    BP.set_motor_dps(BP.PORT_A, target)             # set the target speed for motor A in Degrees Per Second

    print(("Motor A Target Degrees Per Second: %d" % target), "  Motor A Status: ", BP.get_motor_status(BP.PORT_A))

    time.sleep(0.02)
        
    BP.set_motor_power(BP.PORT_A + BP.PORT_B, 100)
    if KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()
    else:
        pass

