import sys
import threading
import odroid_wiringpi as wpi
sys.path.append('./aeac_controls_2022/')
from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
from utils import remap_range
from PID_controller import PID
from encoder import Encoder

def main():
    PIN_A = 27
    PIN_B = 23
    PIN_X = 26
    PIN_Y = 10

    PIN_LJSX = 25
    PIN_LJSY = 29

    uasdriver = UASDriver()

    driver_thread = threading.Thread(target=uasdriver.controlLoop, daemon=True)
    driver_thread.start()

    try:
        while True:
            buttonA = wpi.digitalRead(PIN_A)   # A
            buttonB = wpi.digitalRead(PIN_B)   # B
            buttonX = wpi.digitalRead(PIN_X)   # X
            buttonY = wpi.digitalRead(PIN_Y)  # Y

            raw_ljs_x = wpi.analogRead(PIN_LJSX)
            raw_ljs_y = wpi.analogRead(PIN_LJSY)

            ljs_x, ljs_y = remap_range(raw_ljs_x, raw_ljs_y)

            uasdriver.setRemoteValues(buttonA, buttonB, buttonX, buttonY, ljs_x, ljs_y, 1, 0.0, 0.0, 1)
    except Exception as e:
        print(f"{e}\nExiting UAS Driver Runner.")
        uasdriver.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    main()
