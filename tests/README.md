# Test Suite Descriptions and When to Use Them
The Test suite contains 8 tests, each testing a different part of the system:
 
## 1. Motor Isolation
* This test checks whether power is being supplied properly to each wheel motor.  
* Each motor will be run forward, then back for 3 seconds, one by one.  
* If a motor is not moving on its turn, then something is wrong in the power supply to the wheel, perhaps a bad connection.  

## 2. Encoder Position
* This test checks whether encoders are working and detecting the motor's position properly.  
* Remove the encoder cap and turn the magnet in both directions to observe changes in position on the screen.  
* If position does not change on the screen for a specific motor, or the numbers skip by very large steps (eg. more than 5) at a time when turning the magnet, there is an issue with the encoder connections.  
    * If the position remains stuck at zero, check that everything is connected, and that the 5V and GND pins are not switched. It may help to confirm this with a multimeter.  
    * If the position skips by large steps, the connections might not be secured, or there may be too much noise on the bus, or encA and encB may also be switched.  

## 3. Joystick Calibration
* This test simply observes the cartesian joystick values shown on the screen.  
* Use to confirm the joystick values or tune the thresholds.  

## 4. PID Control
* This test uses the PID controllers along with the encoder signals to move motors to a specific target.  
* Use to confirm that the PID controllers work and that encoder sensors are exact.  
    * If motor position is being updated opposite of the set target and keeps on running, then the motor power wires are likely switched. 
* This can also be used to tune the PID controllers, currently they are tuned at standard values of Kp = 1, Ki = 0, Kd = 0. They have not been tested under load.  

## 5. Joystick Control
* This test runs all 4 wheel motors forward or backward using the Joystick.  
* Use this test to confirm that the wheels respond to the joystick. This can also be used to tune the acceleration multiplier to increase or decrease the acceleration.  

## 6. Drive Test
* This test runs all 4 wheel motors as in the main uasdriver code loop.  
* Use this test to confirm that the wheels respond to the joystick in all directions, and to test the steering code logic. This can also be used to tune the acceleration multiplier to increase or decrease the acceleration.  

## 7. Winch Control (No longer relevant)
* Winch testing, ignore this.  

## 8. Claw Control
* This test controls the 4 actuonix linear actuators using the joystick. Moving the joystick vertically will extend/retract the vertical actuators, and moving the joystick horizontally will extend/retract the horizontal actuators.  
* Use this test to tune the position refreshing rate of the actuators. The actuators already move at the fastest speed, but they are difficult to control, and can be adjusted by change the sleep time. This test also ensures that linear actuators are connected in the correct order to the PWM driver.  

# How to Run a Test?
1. Make sure the stalker code is up to date on the odroid. In the stalker repo: `git pull origin main`.  

2. Make sure the aeac_controls_2022 submodule is up to date: `git submodule update –-remote –-merge`
* **PLEASE use the above command and _NOT_ `git submodule update --init`**. This command does not update the submodule to the latest commit and will result in import errors.  

3. To run the test suite, the code will need to be directly changed on the odroid. First, Identify the test file name that you would like to run, along with the class name (eg. motor_isolation.py and MotorIsolation in aeac_controls_2022/tests/).  

4. Open skystalker.py in a code/text editor on the odroid. Similarily to uasdriver, import the class from the test file at the top of skystalker.py (eg. `from tests.motor_isolation import MotorIsolation`).  

5. Comment out the UASDriver class initialization, and replace it by the class initialization for the test you would like to run (eg. comment out `# uasdriver = UASDriver()` and add `uasdriver = MotorIsolation()` below).  

6. Now run the skystalker code with the usual server set up on the laptop.  