import odroid_wiringpi as wiringpi
import subprocess
import os

PIN_TO_SENSE = 5

def gpio_callback():
    print("GPIO_CALLBACK!")

# unexport all
for pin in range(0, 256):
    file = open("/sys/class/gpio/unexport","w")
    file.write(str(pin))

wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_TO_SENSE, wiringpi.INPUT)
wiringpi.pullUpDnControl(PIN_TO_SENSE, wiringpi.GPIO.PUD_UP)

wiringpi.wiringPiISR(PIN_TO_SENSE, wiringpi.GPIO.INT_EDGE_BOTH, gpio_callback)

while True:
    print(wiringpi.digitalRead(PIN_TO_SENSE))
    wiringpi.delay(2000)