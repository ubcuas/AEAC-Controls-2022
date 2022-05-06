import time
import sys
import math
import logging
import odroid_wiringpi as wpi
sys.path.append('../aeac_controls_2022/')
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

class MotorIsolation:
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

        ############
        # INIT PWM #
        ############
        uaslog.debug("Init PWM...")
        self.pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
        self.pwm.setPWMFreq(FREQUENCY)

        ###############
        # INIT MOTORS #
        ###############
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
        try:
            while True:
                # freq and dc motor testing
                freq = 300
                dc = 60
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
                
        except Exception as e:
            uaslog.warning(f"{e}\nMotor Isolation Test Complete.")
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

        # unexport pins
        for pin in range(0, 256):
            file = open("/sys/class/gpio/unexport","w")
            file.write(str(pin))
        
        uaslog.info("Driver system cleanup complete!")

def main():
    test = MotorIsolation()
    test.controlLoop()

if __name__ == "__main__":
    main()