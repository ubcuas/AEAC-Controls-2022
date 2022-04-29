import time
import sys
import mecanum
import math
import logging
import odroid_wiringpi as wpi
from aeac_controls_2022.pwm import PWM
from aeac_controls_2022.constants import *
from aeac_controls_2022.motor_specs import MOTORS
from aeac_controls_2022.TB9051FTG import TB9051FTG
from aeac_controls_2022.PCA9685 import PCA9685
from aeac_controls_2022.utils import remap_range
from aeac_controls_2022.PID_controller import PID
from aeac_controls_2022.encoder import Encoder

logging.getLogger("Adafruit_I2C.Device.Bus.{0}.Address.{1:#0X}".format(0, 0X40)).setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
uaslog = logging.getLogger("UASlogger")

PIN_A = 27
PIN_B = 23
PIN_X = 26
PIN_Y = 10

PIN_LJSX = 25
PIN_LJSY = 29
        
class JoystickCalibration:
    def __init__(self):
        ######################
        # INIT REMOTE VALUES #
        ######################
        self.buttonA = 1
        self.buttonB = 1
        self.buttonX = 1
        self.buttonY = 1

        self.ljs_x = 0.0
        self.ljs_y = 0.0
        self.ljs_sw = 1
        self.rjs_x = 0.0
        self.rjs_y = 0.0
        self.rjs_sw = 1
        
        uaslog.info("Motor Drive System init complete! Starting main routine...")
    
    def setRemoteValues(self, buttonA, buttonB, buttonX, buttonY, ljs_x, ljs_y, ljs_sw, rjs_x, rjs_y, rjs_sw):
        # joystick movement tolerance
        if ljs_x < THRESHOLD_HIGH and ljs_x > THRESHOLD_LOW:
            ljs_x = 0.0
        if ljs_y < THRESHOLD_HIGH and ljs_y > THRESHOLD_LOW:
            ljs_y = 0.0
        if rjs_x < THRESHOLD_HIGH and rjs_x > THRESHOLD_LOW:
            rjs_x = 0.0

        self.buttonA = buttonA
        self.buttonB = buttonB
        self.buttonX = buttonX
        self.buttonY = buttonY

        self.ljs_x = ljs_x
        self.ljs_y = ljs_y
        self.ljs_sw = ljs_sw
        self.rjs_x = rjs_x
        self.rjs_y = rjs_y
        self.rjs_sw = rjs_sw

        uaslog.debug(f"lSW: {ljs_sw}, lX: {ljs_x}, lY: {ljs_y}, rX: {rjs_x}")

    def controlLoop(self):
        uaslog.info("Starting Joystick Calibration Test...")
        uaslog.info("Joytick Cartesian Values Will be Outputted on Screen.")

        try:
            while True:
                # # READ JOYSTICK
                # raw_ljs_x = wpi.analogRead(PIN_LJSX)
                # raw_ljs_y = wpi.analogRead(PIN_LJSY)

                # self.ljs_x, self.ljs_y = remap_range(raw_ljs_x, raw_ljs_y)

                # if self.ljs_y < THRESHOLD_HIGH and self.ljs_y > THRESHOLD_LOW:
                #     self.ljs_y = 0.0
                # if self.ljs_x < THRESHOLD_HIGH and self.ljs_x > THRESHOLD_LOW:
                #     self.ljs_x = 0.0
                
                print(f"sX: {self.ljs_x:.4f}, sY: {self.ljs_y:.4f}")

        except Exception as e:
            uaslog.warning(f"{e}\nJoystick Calibration Test Complete.")
            sys.exit(0)

    def init_gpio(self):
            uaslog.info("Init GPIO...")
            # unexport pins
            for pin in range(0, 256):
                file = open("/sys/class/gpio/unexport","w")
                file.write(str(pin))

            # setup wpi
            wpi.wiringPiSetup()
            
            # set pin mode
            for pin in GPIO_IN:
                wpi.pinMode(pin, wpi.INPUT)
                wpi.pullUpDnControl(pin, wpi.GPIO.PUD_UP)

            for pin in GPIO_OUT:
                wpi.pinMode(pin, wpi.OUTPUT)
                # init out pins low
                wpi.digitalWrite(pin, 0)
            uaslog.info("Init GPIO complete!")
    
    def cleanup(self):
        uaslog.info("Cleaning up driver system...")

        # unexport pins
        for pin in range(0, 256):
            file = open("/sys/class/gpio/unexport","w")
            file.write(str(pin))

        uaslog.info("Driver system cleanup complete!")

def main():
    test = JoystickCalibration()
    test.controlLoop()
        
if __name__ == "__main__":
    main()