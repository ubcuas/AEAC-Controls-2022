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

# def main2():
#     ##################
#     # INIT GPIO PINS #
#     ##################
#     init_gpio()

#     ############
#     # INIT PWM #
#     ############
#     print("Init PWM...")
#     pwm = PWM(address=I2C_CHIP, busnum=I2C_BUS, debug=False)
#     pwm.setPWMFreq(FREQUENCY)

#     ###############
#     # INIT MOTORS #
#     ###############
#     print("Init Motors...")
#     # ACTUATORS
#     actuonix_1 = PCA9685(channel=CHANNEL8, freq=300)
#     actuonix_1.reset(pwm)
#     actuonix_1.setPWM(pwm, dutycycle=30)

#     # actuonix_2 = PCA9685(channel=CHANNEL9, freq=300)
#     # actuonix_2.reset(pwm)
#     # actuonix_2.setPWM(pwm, dutycycle=60)

#     # actuonix_3 = PCA9685(channel=CHANNEL10, freq=300)
#     # actuonix_3.reset(pwm)
#     # actuonix_3.setPWM(pwm, dutycycle=60)

#     # actuonix_4 = PCA9685(channel=CHANNEL11, freq=300)
#     # actuonix_4.reset(pwm)
#     # actuonix_4.setPWM(pwm, dutycycle=60)
    
#     # SERVO
#     turnigy_1 = PCA9685(channel=CHANNEL12, freq=300)
#     turnigy_1.reset(pwm)
#     turnigy_1.setPWM(pwm, dutycycle=28)

#     # turnigy_2 = PCA9685(channel=CHANNEL13, freq=300)
#     # turnigy_2.reset(pwm)
#     # turnigy_2.setPWM(pwm, dutycycle=28)
    
#     # DC BRUSHED
#     pololu_0 = TB9051FTG(channel=CHANNEL0, freq=300, pin_in=MOTORS["pololu_0"]["enc_pins"], pin_out=MOTORS["pololu_0"]["driver_pins"], single=True)
#     pololu_0.reset(pwm)

#     pololu_1 = TB9051FTG(channel=CHANNEL4, freq=300, pin_in=MOTORS["pololu_1"]["enc_pins"], pin_out=MOTORS["pololu_1"]["driver_pins"])
#     pololu_1.reset(pwm)

#     pololu_2 = TB9051FTG(channel=CHANNEL5, freq=300, pin_in=MOTORS["pololu_2"]["enc_pins"], pin_out=MOTORS["pololu_2"]["driver_pins"])
#     pololu_2.reset(pwm)

#     pololu_3 = TB9051FTG(channel=CHANNEL6, freq=300, pin_in=MOTORS["pololu_3"]["enc_pins"], pin_out=MOTORS["pololu_3"]["driver_pins"])
#     pololu_3.reset(pwm)

#     pololu_4 = TB9051FTG(channel=CHANNEL7, freq=300, pin_in=MOTORS["pololu_4"]["enc_pins"], pin_out=MOTORS["pololu_4"]["driver_pins"])
#     pololu_4.reset(pwm)

#     # INIT PID CONTROLLERS
#     print("Init PID controllers...")
#     pid_1 = PID(MOTORS["pololu_1"]["enc_pins"])
#     pid_2 = PID(MOTORS["pololu_2"]["enc_pins"])
#     pid_3 = PID(MOTORS["pololu_3"]["enc_pins"])
#     pid_4 = PID(MOTORS["pololu_4"]["enc_pins"])

#     # TODO: Remove, TEMP joystick button
#     button_pressed = [0, 0, 0, 1]    # A B X Y
#     joystick_pressed = False

#     # Joystick SW
#     # wpi.pinMode(27, wpi.INPUT)
#     # wpi.pullUpDnControl(27, wpi.GPIO.PUD_UP)

#     PIN_A = 27
#     PIN_B = 23
#     PIN_X = 26
#     PIN_Y = 10
#     ################

#     target_pololu = [0, 0, 0, 0, 0] # p0, p1, p2, p3, p4 = [w, fl, fr, rl, rr]
#     target_actuator = [0, 0]  # a1, a2, a3, a4 = [vertical, horizontal]
#     target_turnigy = [0] #t1, t2 = [in/out]

#     plate_closed = False
#     mode = ControlMode.IDLE

#     print("System init complete! Starting main routine...")

#     try:
#         while True:
#             # freq and dc motor testing
#             # freq = input("Enter freq: ")
#             # dc = input("Enter dc: ")
#             # pwm.setPWMFreq(int(freq))
#             # pololu_1.forward(pwm, dutycycle=int(dc))
#             # pololu_0.forward(pwm, dutycycle=int(dc))

#             # TODO: Remove, Temp code for joystick
#             # A B X Y
#             buttonA = wpi.digitalRead(PIN_A)   # A
#             buttonB = wpi.digitalRead(PIN_B)   # B
#             buttonX = wpi.digitalRead(PIN_X)   # X
#             buttonY = wpi.digitalRead(PIN_Y)  # Y

#             # button debouncing detection
#             while not buttonA:
#                 button_pressed = [1, 0, 0, 0]
#                 buttonA = wpi.digitalRead(PIN_A)
#                 print("DRIVE MODE")
#             while not buttonB:
#                 button_pressed = [0, 1, 0, 0]
#                 buttonB = wpi.digitalRead(PIN_B)
#                 print("WINCH MODE")
#             while not buttonX:
#                 button_pressed = [0, 0, 1, 0]
#                 buttonX = wpi.digitalRead(PIN_X)
#                 print("CLAW MODE")
#             while not buttonY:
#                 button_pressed = [0, 0, 0, 1]
#                 buttonY = wpi.digitalRead(PIN_Y)
#                 print("IDLE MODE")

#             # mode assignment
#             if button_pressed[0]:
#                 mode = ControlMode.DRIVE
#             elif button_pressed[1]:
#                 mode = ControlMode.WINCH
#             elif button_pressed[2]:
#                 mode = ControlMode.CLAW
#             elif button_pressed[3]:
#                 mode = ControlMode.IDLE
#             else:
#                 print("ERROR: mode not recognized, ya screwed up")

#             # TODO: Remove once xbox remote connected
#             # joystick detection
#             # js_sw = wpi.digitalRead(27)
#             js_vrx = wpi.analogRead(25)
#             js_vry = wpi.analogRead(29)
#             # trigger_l = wpi.analogRead(25)
#             # trigger_r = wpi.analogRead(29)

#             sc_vrx, sc_vry= remap_range(js_vrx, js_vry)

#             if sc_vry < 0.2 and sc_vry > -0.2:
#                 sc_vry = 0.0
#             if sc_vrx < 0.2 and sc_vrx > -0.2:
#                 sc_vrx = 0.0

#             # print(f"SW: {js_sw}, sX: {sc_vrx}, sY: {sc_vry}")
#             print(f"sX: {sc_vrx}, sY: {sc_vry}")
#             ################################

#             # move according to mode and joystick ctrls
#             if mode == ControlMode.IDLE:
#                 print("idle")
#                 pass

#             elif mode == ControlMode.DRIVE:
#                 print("drive")
                
#                 # if trigger_l > 0.2 or trigger_r > 0.2:
#                 #     target_pololu = mecanum.setSpinMotorTargets(trigger_l, trigger_r, target_pololu)
#                 # else:
#                 #     # mecanum drive
                
#                 target_pololu = mecanum.setMotorTargets(sc_vrx, sc_vry, 0.0, target_pololu)

#                 print(f"target: {target_pololu}")
#                 print(f"pos: {[0.0, pid_1.getDc(), pid_2.getDc(), pid_3.getDc(), pid_4.getDc()]}")

#                 pid_1.loop(round(target_pololu[1]))
#                 pid_2.loop(round(target_pololu[2]))
#                 pid_3.loop(round(target_pololu[3]))
#                 pid_4.loop(round(target_pololu[4]))

#                 # signal the motors
#                 if pid_1.getDir() == -1:
#                     pololu_1.forward(pwm, dutycycle=pid_1.getDc())
#                 elif pid_1.getDir() == 1:
#                     pololu_1.backward(pwm, dutycycle=pid_1.getDc())
                
#                 if pid_2.getDir() == -1:
#                     pololu_2.forward(pwm, dutycycle=pid_2.getDc())
#                 elif pid_2.getDir() == 1:
#                     pololu_2.backward(pwm, dutycycle=pid_2.getDc())

#                 if pid_3.getDir() == -1:
#                     pololu_3.forward(pwm, dutycycle=pid_3.getDc())
#                 elif pid_3.getDir() == 1:
#                     pololu_3.backward(pwm, dutycycle=pid_3.getDc())

#                 if pid_4.getDir() == -1:
#                     pololu_4.forward(pwm, dutycycle=pid_4.getDc())
#                 elif pid_4.getDir() == 1:
#                     pololu_4.backward(pwm, dutycycle=pid_4.getDc())
            
#             elif mode == ControlMode.WINCH:
#                 print("winch")
#                 if sc_vry > 0.3:
#                     pololu_0.forward(pwm, dutycycle=WINCH_DC_SPEED)
#                 elif sc_vry < -0.3:
#                     pololu_0.backward(pwm, dutycycle=WINCH_DC_SPEED)
#                 else:
#                     pololu_0.backward(pwm, dutycycle=0)

#             elif mode == ControlMode.CLAW:
#                 print("claw")

#                 # VERTICAL ACTUATORS
#                 print(f"DC: {target_actuator[0]}")

#                 # not allowed: 30 & y+, 0 and y-
#                 if not ((math.ceil(target_actuator[0]) >= 30 and sc_vry > -0.1) or (math.floor(target_actuator[0]) == 0 and sc_vry < 0.1)):
#                     target_actuator[0] += sc_vry
#                     actuonix_1.setPWM(pwm, dutycycle=target_actuator[0]+30)
#                     # actuonix_2.setPWM(pwm, dutycycle=target_actuator[0]+30)
#                     time.sleep(0.08)

#                 # HORIZONTAL ACTUATORS
#                 # not allowed: 30 & y+, 0 and y-
#                 if not ((math.ceil(target_actuator[1]) >= 30 and sc_vrx > -0.1) or (math.floor(target_actuator[1]) == 0 and sc_vrx < 0.1)):
#                     target_actuator[1] += sc_vrx
#                     # actuonix_3.setPWM(pwm, dutycycle=target_actuator[1]+30)
#                     # actuonix_4.setPWM(pwm, dutycycle=target_actuator[1]+30)
#                     time.sleep(0.08)

#                 # JOYSTICK SWITCH
#                 while not js_sw:
#                     joystick_pressed = True
#                     js_sw = wpi.digitalRead(27)

#                 if joystick_pressed:
#                     if plate_closed:
#                         plate_closed = False
#                         turnigy_1.setPWM(pwm, dutycycle=28)
#                         # turnigy_2.setPWM(pwm, dutycycle=28)
#                     elif not plate_closed:
#                         plate_closed = True
#                         turnigy_1.setPWM(pwm, dutycycle=56)
#                         # turnigy_2.setPWM(pwm, dutycycle=56)

#                     joystick_pressed = False
#             else:
#                 print("ERROR: mode not recognized :(")

#     except KeyboardInterrupt:
#         actuonix_1.reset(pwm)
#         # actuonix_2.reset(pwm)
#         # actuonix_3.reset(pwm)
#         # actuonix_4.reset(pwm)
#         turnigy_1.reset(pwm)
#         # turnigy_2.reset(pwm)
#         pololu_0.reset(pwm)
#         pololu_1.reset(pwm)
#         pololu_2.reset(pwm)
#         pololu_3.reset(pwm)
#         pololu_4.reset(pwm)
#         cleanup()
#         sys.exit(0)

# def init_gpio():
#     print("Init GPIO...")
#     # unexport pins
#     for pin in range(0, 256):
#         file = open("/sys/class/gpio/unexport","w")
#         file.write(str(pin))

#     # setup wpi
#     wpi.wiringPiSetup()
    
#     # set pin mode
#     for pin in GPIO_IN:
#         wpi.pinMode(pin, wpi.INPUT)
#         wpi.pullUpDnControl(pin, wpi.GPIO.PUD_UP)

#     for pin in GPIO_OUT:
#         wpi.pinMode(pin, wpi.OUTPUT)
#         # init out pins low
#         wpi.digitalWrite(pin, 0)
#     print("Init GPIO complete!")

# def cleanup():
#     print("Cleaning up...")
#     # unexport pins
#     for pin in range(0, 256):
#         file = open("/sys/class/gpio/unexport","w")
#         file.write(str(pin))
# print("Cleanup complete!")

