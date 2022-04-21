import time
import sys
import math
import logging
import odroid_wiringpi as wpi
from pwm import PWM
from uas_control_system.constants import *
from uas_control_system.motor_specs import MOTORS
from uas_control_system.TB9051FTG import TB9051FTG
from uas_control_system.PCA9685 import PCA9685
from uas_control_system.utils import remap_range
from uas_control_system.PID_controller import PID
from uas_control_system.encoder import Encoder

logging.getLogger("Adafruit_I2C.Device.Bus.{0}.Address.{1:#0X}".format(0, 0X40)).setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
uaslog = logging.getLogger("UASlogger")

class MotorIsolation:
    def __init__(self):
        ##################
        # INIT GPIO PINS #
        ##################
        self.init_gpio()

        ############
        # INIT PWM #
        ############
        uaslog.debug("Init PWM...")
        self.pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
        self.pwm.setPWMFreq(FREQUENCY)

        # ###############
        # # INIT MOTORS #
        # ###############
        uaslog.debug("Init Motors...")
        # DC BRUSHED
        self.pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
        self.pololu_1.reset(self.pwm)

        self.pololu_2 = TB9051FTG(channel=CHANNEL5, freq=300, pin_in=MOTORS["pololu_2"]["enc_pins"], pin_out=MOTORS["pololu_2"]["driver_pins"])
        self.pololu_2.reset(self.pwm)

        self.pololu_3 = TB9051FTG(channel=CHANNEL6, freq=300, pin_in=MOTORS["pololu_3"]["enc_pins"], pin_out=MOTORS["pololu_3"]["driver_pins"])
        self.pololu_3.reset(self.pwm)

        self.pololu_4 = TB9051FTG(channel=CHANNEL7, freq=300, pin_in=MOTORS["pololu_4"]["enc_pins"], pin_out=MOTORS["pololu_4"]["driver_pins"])
        self.pololu_4.reset(self.pwm)

    def loop(self):
        try:
            while True:
                # freq and dc motor testing
                freq = input("Enter freq: ")
                dc = input("Enter dc: ")
                self.pwm.setPWMFreq(int(freq))

                uaslog.info("Starting Motor Isolation Test...")
                uaslog.info("Each motor will be run forward then back for 3 seconds individually.")

                uaslog.info("Running Pololu 1 Position {}".format(MOTORS["pololu_1"]["position"]))
                uaslog.info("Forward...")
                self.pololu_1.forward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                uaslog.info("Backward...")
                self.pololu_1.backward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                self.pololu_1.reset(self.pwm)

                uaslog.info("Running Pololu 2 Position {}".format(MOTORS["pololu_2"]["position"]))
                uaslog.info("Forward...")
                self.pololu_2.forward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                uaslog.info("Backward...")
                self.pololu_2.backward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                self.pololu_2.reset(self.pwm)

                uaslog.info("Running Pololu 3 Position {}".format(MOTORS["pololu_3"]["position"]))
                uaslog.info("Forward...")
                self.pololu_3.forward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                uaslog.info("Backward...")
                self.pololu_3.backward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                self.pololu_3.reset(self.pwm)

                uaslog.info("Running Pololu 4 Position {}".format(MOTORS["pololu_4"]["position"]))
                uaslog.info("Forward...")
                self.pololu_4.forward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                uaslog.info("Backward...")
                self.pololu_4.backward(self.pwm, dutycycle=int(dc))
                time.sleep(3)
                self.pololu_4.reset(self.pwm)

                uaslog.info("Motor Isolation Test Complete!")
                self.cleanup()
                sys.exit(0)
                
        except KeyboardInterrupt:
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
        # reset motors
        self.pololu_1.reset(self.pwm)
        self.pololu_2.reset(self.pwm)
        self.pololu_3.reset(self.pwm)
        self.pololu_4.reset(self.pwm)

def main():
    test = MotorIsolation()
    test.loop()

if __name__ == "__main__":
    main()