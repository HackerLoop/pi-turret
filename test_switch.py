#!/bin/env python

import signal
import sys
import time

import RPi.GPIO as GPIO

SLOW_SWITCH=27
FAST_SWITCH=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(SLOW_SWITCH, GPIO.OUT)
GPIO.setup(FAST_SWITCH, GPIO.OUT)
GPIO.output(SLOW_SWITCH, False)
GPIO.output(FAST_SWITCH, False)

def signal_handler(signal, frame):
    GPIO.output(SLOW_SWITCH, False)
    GPIO.output(FAST_SWITCH, False)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print('SLOW')
GPIO.output(SLOW_SWITCH, True)
time.sleep(2)
print('FAST')
GPIO.output(FAST_SWITCH, True)
time.sleep(2)
GPIO.output(SLOW_SWITCH, False)
GPIO.output(FAST_SWITCH, False)
