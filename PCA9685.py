""" This class is an instance of a single PCA9685 board PWM channel """

from constants import *
from utils import getCounterValues
from pwm import PWM

class PCA9685:
    def __init__(self, channel, freq, debug=False):
        self.freq = freq
        self.current_state = 0 #
        self.channel = channel
        self.debug = debug

    def reset(self, pwm):
        # reset PCA9685
        if self.debug:
            print("Reseting PCA9685")
        on_count, off_count = getCounterValues(delay=0, dc=0)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)  # EN = 0

    def setPWM(self, pwm, dutycycle, delay=0):
        on_count, off_count = getCounterValues(delay, dutycycle)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)

        if self.debug:
            print("Delay: {}, Duty Cycle: {}".format(delay, dutycycle))
            print("ON: {}, {}, OFF: {}, {}".format(on_count, hex(on_count), off_count, hex(off_count)))
        
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)


