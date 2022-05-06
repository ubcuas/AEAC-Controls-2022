# PID loop controller for motor encoder
import time
import logging
import sys
sys.path.append('./aeac_controls_2022/')
from constants import MAX_DC, MIN_DC
from encoder import Encoder
from utils import pwmToDc

logging.basicConfig(level=logging.DEBUG)
uaslog = logging.getLogger("UASlogger")

class PID:
    def __init__(self, enc_pins, target=0, debug=False):
        self.target = target
        self.pos = 0
        self.dir = 0
        self.dc = 0

        self.prevT = float(0)
        self.eprev = float(0)
        self.eintegral = float(0)
        self.debug = debug

        self.enc = Encoder(enc_pins) # callback = updatePos

    def loop(self, target):
        self.target = target

        # PID constants
        # TODO: tune params - init 1.0, 0.0, 0.0
        kp = float(1.0)
        kd = float(0.0)
        ki = float(0.0)

        # current pos
        self.pos = self.enc.getPos()

        # time difference
        currT = time.time()
        deltaT = float(currT - self.prevT)
        self.prevT = currT

        # error
        e = self.pos - self.target

        # derivative
        dedt = (e - self.eprev)/(deltaT)

        # integral
        self.eintegral = self.eintegral + e*deltaT

        # control signal
        u = float(kp*e + kd*dedt + ki*self.eintegral)

        # motor power
        pwr = float(abs(u))
        if pwr > 255:
            pwr = 255
            
        self.dc = pwmToDc(pwr)
        if self.dc > MAX_DC:
            self.dc = MAX_DC
        elif self.dc < MIN_DC:
            self.dc = 0
            
        # motor direction
        self.dir = 1
        if u < 0:
            self.dir = -1

        # store previous error
        self.eprev = e

        if self.debug:
            print(f"target: {self.target} pos: {self.pos}, pwr: {pwr}, dc: {self.dc}, e: {e}")

    def getDir(self):
        return self.dir

    def getPos(self):
        return self.pos

    def getDc(self):
        return self.dc

def updatePosCallback(pos):
    uaslog.info("New position: {}".format(pos))