from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
from utils import remap_range
import odroid_wiringpi as wpi
import time
import sys
import mecanum
from PID_controller import PID
from encoder import Encoder
import math

import threading
from uasdriver import UASDriver

def main():
    PIN_A = 27
    PIN_B = 23
    PIN_X = 26
    PIN_Y = 10

    PIN_LJSX = 25
    PIN_LJSY = 29

    uasdriver = UASDriver()

    driver_thread = threading.Thread(target=uasdriver.controlLoop)
    driver_thread.start()

    while True:
        buttonA = wpi.digitalRead(PIN_A)   # A
        buttonB = wpi.digitalRead(PIN_B)   # B
        buttonX = wpi.digitalRead(PIN_X)   # X
        buttonY = wpi.digitalRead(PIN_Y)  # Y

        raw_ljs_x = wpi.analogRead(PIN_LJSX)
        raw_ljs_y = wpi.analogRead(PIN_LJSY)

        ljs_x, ljs_y = remap_range(raw_ljs_x, raw_ljs_y)

        uasdriver.setRemoteValues(buttonA, buttonB, buttonX, buttonY, ljs_x, ljs_y, 1, 0.0, 0.0, 1)

if __name__ == "__main__":
    main()
