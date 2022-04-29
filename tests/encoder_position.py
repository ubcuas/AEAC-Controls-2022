import time
import sys
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
        
class EncoderPosition:
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

        ##################
        # INIT GPIO PINS #
        ##################
        self.init_gpio()

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
        uaslog.info("Starting Encoder Position Sensing Test...")
        uaslog.info("Remove Encoder Cap and Turn the Magnet in Both Direction to Observe Changes in Position.")

        enc1 = Encoder(MOTORS["pololu_1"]["enc_pins"])
        enc2 = Encoder(MOTORS["pololu_2"]["enc_pins"])
        enc3 = Encoder(MOTORS["pololu_3"]["enc_pins"])
        enc4 = Encoder(MOTORS["pololu_4"]["enc_pins"])

        try:
            while True:
                print(f"Position enc1: {enc1.getPos()}, enc2: {enc2.getPos()}, enc3: {enc3.getPos()}, enc4: {enc4.getPos()}")
                time.sleep(0.5)
                
        except Exception as e:
            uaslog.warning(f"{e}\nEncoder Position Sensing Test Complete.")
            self.cleanup()
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

def updatePosCallback(pos):
    uaslog.info("New position: {}".format(pos))

def main():
    test = EncoderPosition()
    test.controlLoop()
        
if __name__ == "__main__":
    main()