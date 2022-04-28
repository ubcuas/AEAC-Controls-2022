import threading
import sys
from encoder import Encoder
import odroid_wiringpi as wpi
from utils import remap_range

from tests.motor_isolation import MotorIsolation
from tests.encoder_position import EncoderPosition
from tests.joystick_calibration import JoystickCalibration
from tests.pid_control import PIDControl
from tests.joystick_control import JoystickControl
from tests.drive_test import DriveTest
from tests.winch_control import WinchControl
from tests.claw_control import ClawControl

def main():
    PIN_A = 27
    PIN_B = 23
    PIN_X = 26
    PIN_Y = 10

    PIN_LJSX = 25
    PIN_LJSY = 29

    test = input("Select test to run:\n(1) Motor Isolation\n(2) Encoder Position\n(3) Joystick Calibration\n(4) PID Control\n(5) Joystick Control\n(6) Drive Test\n(7) Winch Control\n(8) Claw Control\n")

    wpi.wiringPiSetup()

    if test == "1":
        uastester = MotorIsolation()
    elif test == "2":
        uastester = EncoderPosition()
    elif test == "3":
        uastester = JoystickCalibration()
    elif test == "4":
        uastester = PIDControl()
    elif test == "5":
        uastester = JoystickControl()
    elif test == "6":
        uastester = DriveTest()
    elif test == "7":
        uastester = WinchControl()
    elif test == "8":
        uastester = ClawControl()
    else:
        print("Enter a valid number >:(")
        sys.exit(0)

    tester_thread = threading.Thread(target=uastester.loop)
    tester_thread.start()

    try:
        while True:
            buttonA = wpi.digitalRead(PIN_A)   # A
            buttonB = wpi.digitalRead(PIN_B)   # B
            buttonX = wpi.digitalRead(PIN_X)   # X
            buttonY = wpi.digitalRead(PIN_Y)   # Y

            raw_ljs_x = wpi.analogRead(PIN_LJSX)
            raw_ljs_y = wpi.analogRead(PIN_LJSY)

            ljs_x, ljs_y = remap_range(raw_ljs_x, raw_ljs_y)

            uastester.setRemoteValues(buttonA, buttonB, buttonX, buttonY, ljs_x, ljs_y, 1, 0.0, 0.0, 1)
            
    except KeyboardInterrupt:
        uastester.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
