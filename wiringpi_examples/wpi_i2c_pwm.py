#!/usr/bin/python

import time
import math
import odroid_wiringpi as wpi
from constants import *

# ============================================================================
# Adafruit PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PWM :
    i2c = None

    # need busnum, i2c_interface
    def __init__(self, busnum=0, address=0x40, debug=False):
        # wpi set up
        wpi.wiringPiSetup()
        self.i2c = wpi.wiringPiI2CSetupInterface(busnum, address)

        self.address = address
        self.debug = debug

        # reset PCA9685
        if self.debug:
            print("Reseting PCA9685")
        wpi.wiringPiI2CWriteReg8(self.i2c, MODE1, 0x00)

    def setPWMFreq(self, freq):
        """ Sets the PWM frequency """

        prescaleval = ((CLK/COUNTER_SIZE)/float(freq)) - 1.0   # 25MHz

        if self.debug:
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)

        prescale = math.floor(prescaleval + 0.5)

        if self.debug:
            print("Final pre-scale: %d" % prescale)

        oldmode = wpi.wiringPiI2CReadReg8(self.i2c, MODE1)
        newmode = (oldmode & 0x7F) | 0x10             # sleep

        wpi.wiringPiI2CWriteReg8(self.i2c, MODE1, newmode)        # go to sleep
        wpi.wiringPiI2CWriteReg8(self.i2c, PRESCALE, int(math.floor(prescale)))
        wpi.wiringPiI2CWriteReg8(self.i2c, MODE1, oldmode)

        time.sleep(0.005)
        wpi.wiringPiI2CWriteReg8(self.i2c, MODE1, oldmode | 0x80)

    # TODO: set PWM by frequency and duty cycle
    def setPWMCounters(self, channel, on, off):
        """Sets a single PWM channel"""

        wpi.wiringPiI2CWriteReg8(self.i2c, LED0_ON_L + 4*channel, on & 0xFF)
        wpi.wiringPiI2CWriteReg8(self.i2c, LED0_ON_H + 4*channel, on >> 8)
        wpi.wiringPiI2CWriteReg8(self.i2c, LED0_OFF_L + 4*channel, off & 0xFF)
        wpi.wiringPiI2CWriteReg8(self.i2c, LED0_OFF_H + 4*channel, off >> 8)

def main():
    pwm = PWM(address=I2C_CHIP, busnum=I2C_DEV, debug=True)
    pwm.setPWMFreq(300) # 50 for analog servos, 300 for digital servos
    pwm.setPWMCounters(I2C_BUS, 0x199, 0x666)

if __name__ == "__main__":
    main()