#!/bin/env python

import time

import RPi.GPIO as GPIO

NERF_TRIGGER = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(NERF_TRIGGER, GPIO.OUT)
GPIO.setup(NERF_TRIGGER + 1, GPIO.OUT)

while True :
    print('up')
    GPIO.output(NERF_TRIGGER, False)
    GPIO.output(NERF_TRIGGER+1, True)

    time.sleep(3);

    print('down')
    GPIO.output(NERF_TRIGGER, True)
    GPIO.output(NERF_TRIGGER + 1, False)

    time.sleep(3);
