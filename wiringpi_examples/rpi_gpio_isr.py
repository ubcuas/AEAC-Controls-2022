#!/usr/bin/env python3

import sys
import time
import RPi.GPIO as GPIO

# https://wiki.odroid.com/odroid-xu4/application_note/gpio/rpi.gpio#about_bcm_numbering
IRQ_GPIO_PIN = 4
IRQ_EDGE = GPIO.FALLING
count = 0

def handler(channel):
    global count

    count += 1

def print_status():
    global count

    print(count)
    count = 0

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IRQ_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(IRQ_GPIO_PIN, IRQ_EDGE, callback=handler)

    print('Press Ctrl-C to exit')
    try:
        while True:
            time.sleep(1)
            print_status()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)