#!/usr/bin/python3
import odroid_wiringpi as wpi

# Prerequisites:
# * wiringPi: http://odroid.com/dokuwiki/doku.php?id=en:c1_tinkering#python_example
                                                                    
#initialize wiringPi                        
wpi.wiringPiSetup()                                                                 
                                                                                           
pwmPin = 7 #GPIO 249 on Odroid C2, Pin 7
brightness = 70 #percent

#set as output pin 
wpi.pinMode(pwmPin, 1)

wpi.softPwmCreate(pwmPin,0,100) # Setup PWM using Pin, Initial Value and Range parameters
while True:
    wpi.softPwmWrite(pwmPin,brightness) # Change PWM duty cycle