#!/usr/bin/python
import sys
import odroid_wiringpi as wpi
sys.path.append('./aeac_controls_2022/')
from constants import I2C_BUS
from utils import getCounterValues

class TB9051FTG:
    # inputs = [encA, encB]
    # outputs = [ENB, PWM1, PWM2]
    def __init__(self, channel, freq, pin_in, pin_out, single=False, debug=False):
        self.freq = freq
        self.current_state = 0
        self.channel = channel
        self.debug = debug
        self.single = single    # dual channel by default

        # odroid - motor/driver input and output pins
        self.pin_in = pin_in    # encA encB
        self.pin_out = pin_out  # dir en enb # en pwm1 pwm2

    def reset(self, pwm):
        # reset TB9051FTG
        if self.debug:
            print("Reseting TB9051FTG")
        on_count, off_count = getCounterValues(delay=0, dc=0)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)  # EN = 0

    def forward(self, pwm, dutycycle):
        wpi.digitalWrite(self.pin_out[0], 1)    # dir/pwm1 1

        if self.single:
            wpi.digitalWrite(self.pin_out[1], 0)    # en 1/pwm2 0
        else:
            wpi.digitalWrite(self.pin_out[1], 1)    # en 1/pwm2 0

        self.setPWM(pwm, dutycycle)
    
    def backward(self, pwm, dutycycle):
        wpi.digitalWrite(self.pin_out[0], 0)    # dir/pwm1 0
        wpi.digitalWrite(self.pin_out[1], 1)    # en/pwm2 1

        self.setPWM(pwm, dutycycle)
    
    def brake(self, pwm):
        wpi.digitalWrite(self.pin_out[1], 1)    # en/ 1

        self.setPWM(pwm, 0)

    def setPWM(self, pwm, dutycycle, delay=0):
        on_count, off_count = getCounterValues(delay, dutycycle)
        on_hex, off_hex = int(hex(on_count), base=16), int(hex(off_count), base=16)

        if self.debug:
            print("Delay: {}, Duty Cycle: {}".format(delay, dutycycle))
            print("ON: {}, {}, OFF: {}, {}".format(on_count, hex(on_count), off_count, hex(off_count)))
        pwm.setPWMCounters(self.channel, I2C_BUS, on_hex, off_hex)


