#!/usr/bin/python

from Adafruit_Thermal import *
import time
#import random
import math
from make_piece import create_rotated_line_image
from get_weather import get_ulyanovsk_weather, API_KEY
from dht import get_temp_humidity

printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)



INTERVAL = 900 
timestep_inpxs = 40
range_step = 2

#temp0 = random.uniform(25,26)

while True: 
    temp0,humid0 = get_temp_humidity()
    if temp0:
        break 
temp_range0 = (int(temp0)-range_step, int(temp0)+range_step)
print(f'Initial temp range is {temp_range0}')

counter =0
point1 = (20, temp0)  # (x координата, температура)
while True:
    #newtemp = random.uniform(29,30)
    newtemp,newhumid = get_temp_humidity() 
    if (newtemp):
            if newtemp > temp_range0[1]:
                    temp_range2 = (temp_range0[0]+math.ceil(abs(newtemp-temp_range0[1])),math.ceil(newtemp))
                    print(f'Value is above high limit {temp_range2}')
            else:
                    if newtemp < temp_range0[0]:
                        temp_range2 = (math.floor(newtemp),temp_range0[1]-math.ceil(abs(newtemp-temp_range0[0])))
                        print(f'Value is under low limit {temp_range2}')
                    else:
                        temp_range2 = temp_range0
                        print(f'Value is in the range {temp_range2}')
            newpoint = (point1[0]+timestep_inpxs,newtemp)
            image = create_rotated_line_image(point1, newpoint, temp_range0,temp_range2, 
					line_width=2, marker_size=5)
            printer.printImage(image)
            counter = counter +1	
            print(f"New point is :{counter}.{newpoint}")
            point1 = (point1[0],newtemp)
            temp_range0 = temp_range2 

    time.sleep(INTERVAL)


printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
