# pololu class and encoder?
import odroid_wiringpi as wpi
from constants import *
from motor_specs import MOTORS

class Encoder:
    def __init__(self, enc, callback=None):
        self.encA = enc[0]
        self.encB = enc[1]

        self.pos = 0
        self.dir = None

        self.callback = callback

        # ENCODER INTERRUPT
        wpi.wiringPiISR(self.encA, wpi.GPIO.INT_EDGE_RISING, self.readEncoder) #encA

    def readEncoder(self):
        encB = wpi.digitalRead(self.encB)    # encB

        if encB > 0:
            self.pos += 1
        else:
            self.pos -= 1

        if self.callback != None:
            self.callback(self.pos)
    
    def getPos(self):
        return self.pos