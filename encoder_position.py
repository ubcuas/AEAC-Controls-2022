import time
import sys
import mecanum
import math
import logging
import odroid_wiringpi as wpi
from pwm import PWM
from constants import *
from motor_specs import MOTORS
from TB9051FTG import TB9051FTG
from PCA9685 import PCA9685
from utils import remap_range
from PID_controller import PID
from encoder import Encoder

logging.getLogger("Adafruit_I2C.Device.Bus.{0}.Address.{1:#0X}".format(0, 0X40)).setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
uaslog = logging.getLogger("UASlogger")
        
class EncoderPosition:
    def __init__(self):

        ##################
        # INIT GPIO PINS #
        ##################
        self.init_gpio()

        uaslog.info("Motor Drive System init complete! Starting main routine...")
        
    def loop(self):
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
                
        except KeyboardInterrupt:
            uaslog.info("Encoder Position Sensing Test Complete!")
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
    test.loop()
        
if __name__ == "__main__":
    main()