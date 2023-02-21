import math
import time
import numpy as np
import random
import brickpi3
# from __future__ import print_function # use python 3 syntax but make it compatible with python 2
# from __future__ import division       #   
BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_ULTRASONIC)
while True:
        # read and display the sensor value
        # BP.get_sensor retrieves a sensor value.
        # BP.PORT_1 specifies that we are looking for the value of sensor port 1.
        # BP.get_sensor returns the sensor value (what we want to display).
        try:
            value = BP.get_sensor(BP.PORT_1)
            print(value)                         # print the distance in CM
        except brickpi3.SensorError as error:
            print(error)
        time.sleep(0.1)