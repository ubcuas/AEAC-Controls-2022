# UBC UAS Ground Control System - AEAC 2022 Competition
The Ground Electrical and Control System for UBC UAS Ataksak drone interfacing with an Odroid XU4. Includes PID controllers for a mecanum drive landing gear, winch, and claw controlled by an Xbox Remote.  

## XBox Controls
### Modes: 
* **BTN A: Drive**
    * Use left joystick to control the mecanum drive
* **BTN B: Winch**
    * Use left joystick Y axis to lower/raise winch system
* **BTN X: Claw**
    * Use left joystick Y axis to extend/retract claw vertical actuators
    * Use left joystick X axis to extend/retract claw horizontal actuators
    * Use left joystick SW button to turn claw bottom plates inward to secure package
* **BTN Y: Idle**
    * Initial control mode

## System Schematics and Wiring
The system consists of:  
* 1 Laptop (Ground Control)
* 1 Odroid XU4 Single Board Computer (Sky Control)
* 2 TB9051FTG Dual Channel Brushed Motor Drivers for the Mecanum Drive
* 1 Single TB9041FTG Single Channel Brushed Motor Driver for the Winch Motor
* 1 16-Channel PCA9685 I2C-PWM Driver
* 4 Encoded 12V HP Pololu Motors for the Mecanum Drive
* 1 Unencoded 12V HP Pololu Motor for the Winch
* 4 100cm Actuonix Linear Actuators for the Claw
* 2 Turnigy Digital Servo Motors for the Claw's Bottom Plate
* 3S Lipo Battery
* Low Pass Filters to filter out noise on encoder channels
* 5V Rails
A full (sketchy and handrawn) schematics of the wire connections and boards is shown here: https://github.com/Abeilles14/uas_control_system/blob/main/Schematics%20%26%20Connections%20Rev%20A.pdf  

## System Integration Test Suite
A complete test suite testing each individual component of the system in isolation was created. See here for test descriptions, debugging tips, and when to use them: https://github.com/Abeilles14/uas_control_system/blob/main/tests/README.md  

## Connecting the Xbox Controller
The Xbox controller is connected via bluetooth or cable to Ground Control. A Cellular modem is connected to the Odroid. Xbox controls are sent to the Odroid remotely through websocket.  
An SSH tunnel is first opened on Ground Control for port forwarding. The GroundStalker server is run on Ground Control in order to send Xbox controls to the Odroid, and the Odroid is accessed by SSH to run SkyStalker and receive XBox remote commands. The motor drivers and control systems in this repository are run as a submodule of SkyStalker.  
All SSH functions are managed by VPS on Termius for convenience.  

### Requirements and Libraries
adafruit-blinka  
adafruit-extended-bus  
Adafruit_GPIO  
i2c-tools  

