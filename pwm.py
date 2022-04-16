#!/usr/bin/python

import time
import math
from Adafruit_GPIO.I2C import Device as Adafruit_I2C
from constants import *
from utils import getCounterValues

# ============================================================================
# Adafruit PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PWM :
    i2c = None

    # need busnum, i2c_interface
    def __init__(self, address=0x40, busnum=0, debug=False):
        self.i2c = Adafruit_I2C(address, busnum)

        self.address = address
        self.debug = debug

        if self.debug:
            print("Reseting PCA9685")
            
        self.i2c.write8(MODE1, 0x00)

    def setPWMFreq(self, freq):
        """ Sets the PWM frequency """

        prescaleval = ((CLK/COUNTER_SIZE)/float(freq)) - 1.0   # 25MHz

        if self.debug:
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)

        
        prescale = math.floor(prescaleval + 0.5)
       
        if self.debug:
            print("Final pre-scale: %d" % prescale)

        oldmode = self.i2c.readU8(MODE1);
        newmode = (oldmode & 0x7F) | 0x10             # sleep
       
        self.i2c.write8(MODE1, newmode)        # go to sleep
        self.i2c.write8(PRESCALE, int(math.floor(prescale)))
        self.i2c.write8(MODE1, oldmode)
        
        time.sleep(0.005)
        
        self.i2c.write8(MODE1, oldmode | 0x80)

    def setPWMCounters(self, reg, bus, on, off):
        """Sets a single PWM channel"""

        if self.debug:
            print("Setting PWM at reg {} bus {}".format(reg, bus))

        self.i2c.write8(reg[0] + 4*bus, on & 0xFF)
        self.i2c.write8(reg[1] + 4*bus, on >> 8)
        self.i2c.write8(reg[2] + 4*bus, off & 0xFF)
        self.i2c.write8(reg[3] + 4*bus, off >> 8)

