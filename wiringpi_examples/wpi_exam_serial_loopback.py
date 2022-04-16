#!/usr/bin/env python
import odroid_wiringpi as wpi
import time
 
serial = wpi.serialOpen("/dev/ttySAC0", 115200)
 
while True:
	input_str = input("Serial Input> ")
	wpi.serialPuts(serial, input_str)
	time.sleep(0.1)

	output_str = "Serial Output> "
	output_str += chr(wpi.serialGetchar(serial))
	print(output_str)
 
wpi.serialClose(serial)