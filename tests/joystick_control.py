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
        
class JoystickControl:
    def __init__(self):
        ############################
        # INIT MOTOR TARGET VALUES #
        ############################
        self.target_pololu = [0, 0, 0, 0, 0] # p0, p1, p2, p3, p4 = [w, fl, fr, rl, rr]

        ######################
        # INIT REMOTE VALUES #
        ######################
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

        ########################
        # INIT PID CONTROLLERS #
        ########################
        uaslog.debug("Init PID controllers...")
        self.pid_1 = PID(MOTORS["pololu_1"]["enc_pins"], debug=True)
        self.pid_2 = PID(MOTORS["pololu_2"]["enc_pins"])
        self.pid_3 = PID(MOTORS["pololu_3"]["enc_pins"])
        self.pid_4 = PID(MOTORS["pololu_4"]["enc_pins"])

        uaslog.info("Motor Drive System init complete! Starting main routine...")
    
    def setRemoteValues(self, buttonA, buttonB, buttonX, buttonY, ljs_x, ljs_y, ljs_sw, rjs_x, rjs_y, rjs_sw):
        # joystick movement tolerance
        if self.ljs_x < THRESHOLD_HIGH and ljs_x > THRESHOLD_LOW:
            self.ljs_x = 0.0
        if self.ljs_y < THRESHOLD_HIGH and ljs_y > THRESHOLD_LOW:
            self.ljs_y = 0.0
        if self.rjs_x < THRESHOLD_HIGH and rjs_x > THRESHOLD_LOW:
            self.rjs_x = 0.0

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
        uaslog.info("Starting Joystick Motor Control Test...")
        uaslog.info("Joystick will control wheels to move forward or backward.")

        try:
            while True:
                # READ JOYSTICK
                # raw_ljs_x = wpi.analogRead(PIN_LJSX)
                # raw_ljs_y = wpi.analogRead(PIN_LJSY)

                # self.ljs_x, self.ljs_y = remap_range(raw_ljs_x, raw_ljs_y)

                # if self.ljs_y < THRESHOLD_HIGH and self.ljs_y > THRESHOLD_LOW:
                #     self.ljs_y = 0.0
                # if self.ljs_x < THRESHOLD_HIGH and self.ljs_x > THRESHOLD_LOW:
                #     self.ljs_x = 0.0
                
                # print(f"sX: {self.ljs_x:.4f}, sY: {self.ljs_y:.4f}")

                # SET MOTOR TARGETS
                # set 1 and 4 reverse due to wheel orientation.
                self.target_pololu[1] -= self.ljs_y * ACCEL_MULTIPLIER
                self.target_pololu[2] += self.ljs_y * ACCEL_MULTIPLIER
                self.target_pololu[3] += self.ljs_y * ACCEL_MULTIPLIER
                self.target_pololu[4] -= self.ljs_y * ACCEL_MULTIPLIER
                
                # print(f"target pos: [{self.target_pololu[1]:.4f}]")
                print(f"target pos: [{self.target_pololu[1]:.4f}, {self.target_pololu[2]:.4f}, {self.target_pololu[3]:.4f}, {self.target_pololu[4]:.4f}]")

                self.pid_1.loop(round(self.target_pololu[1]))
                self.pid_2.loop(round(self.target_pololu[2]))
                self.pid_3.loop(round(self.target_pololu[3]))
                self.pid_4.loop(round(self.target_pololu[4]))

                # signal the motors
                if self.pid_1.getDir() == -1:
                    self.pololu_1.forward(self.pwm, dutycycle=self.pid_1.getDc())
                elif self.pid_1.getDir() == 1:
                    self.pololu_1.backward(self.pwm, dutycycle=self.pid_1.getDc())
                
                if self.pid_2.getDir() == -1:
                    self.pololu_2.forward(self.pwm, dutycycle=self.pid_2.getDc())
                elif self.pid_2.getDir() == 1:
                    self.pololu_2.backward(self.pwm, dutycycle=self.pid_2.getDc())

                if self.pid_3.getDir() == -1:
                    self.pololu_3.forward(self.pwm, dutycycle=self.pid_3.getDc())
                elif self.pid_3.getDir() == 1:
                    self.pololu_3.backward(self.pwm, dutycycle=self.pid_3.getDc())

                if self.pid_4.getDir() == -1:
                    self.pololu_4.forward(self.pwm, dutycycle=self.pid_4.getDc())
                elif self.pid_4.getDir() == 1:
                    self.pololu_4.backward(self.pwm, dutycycle=self.pid_4.getDc())
                
                # print(f"curr pos: [{self.pid_1.getPos()}]")
                print(f"curr pos: [{self.pid_1.getPos()}, {self.pid_2.getPos()}, {self.pid_3.getPos()}, {self.pid_4.getPos()}, ]")
                
        except KeyboardInterrupt:
            uaslog.info("Joystick Control Test Complete!")
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
    test = JoystickControl()
    test.controlLoop()
        
if __name__ == "__main__":
    main()