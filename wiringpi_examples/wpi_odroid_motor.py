#!/usr/bin/env python
# PCA9685 has 25 MHz internal clk to generate PWM

import odroid_wiringpi as wpi
import time

i2c_dev = "/dev/i2c-0"      # device
# I2C slave address for device, default is 0x40
i2c_addr = 0x40             # device address

wpi.wiringPiSetup()
i2c_fd = wpi.wiringPiI2CSetupInterface(i2c_dev, i2c_addr)

# reg = wpi.wiringPiI2CWrite(i2c_fd, 0xFF)         # Simple device write. Some devices accept data this way without needing to access any internal registers.
# print(reg)
# reg = wpi.wiringPiI2CReadReg8(i2c_fd, 0x00)            # These read an 8-bit value from the device register(0x00) indicated.
# reg = wpi.wiringPiI2CWriteReg16(i2c_fd, 0x10, 0x1234)  # These write an 16-bit data value into the device register(0x10) indicated.
# print(reg)

# Reset PCA9685


# WRITE LED0_ON_H
reg = wpi.wiringPiI2CWriteReg8(i2c_fd, 0x07, 0x01)
print(reg)
# WRITE LED0_ON_L
reg = wpi.wiringPiI2CWriteReg8(i2c_fd, 0x06, 0x99)
print(reg)
# WRITE LED0_OFF_H
reg = wpi.wiringPiI2CWriteReg8(i2c_fd, 0x09, 0x06)
print(reg)
# WRITE LED0_OFF_L
reg = wpi.wiringPiI2CWriteReg8(i2c_fd, 0x08, 0x66)
print(reg)

reg = wpi.wiringPiI2CReadReg8(i2c_fd, 0x07)
print(reg)
reg = wpi.wiringPiI2CRead(i2c_fd)                      # Simple device read. Some devices present data when you read them without having to do any register transactions.
print(reg)

# wpi.wiringPiSetup()
# wpi.pinMode(0, 1)
 
# while True:
#     wpi.digitalWrite(0, 1)
#     time.sleep(1)
#     wpi.digitalWrite(0, 0)
#     time.sleep(1)


