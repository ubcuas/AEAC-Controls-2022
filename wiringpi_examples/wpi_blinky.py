#!/usr/bin/env python
 
import odroid_wiringpi as wpi
import time
 
wpi.wiringPiSetup()
wpi.pinMode(0, 1)
 
while True:
    wpi.digitalWrite(27, 1)
    time.sleep(1)
    wpi.digitalWrite(27, 0)
    time.sleep(1)