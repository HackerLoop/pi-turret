#!/bin/env python

import sys

import time

import RPi.GPIO as GPIO

NERF_TRIGGER_1 = 14
NERF_TRIGGER_2 = 15

NERF_TRIGGER_RETURN = 18

SLOW_SWITCH=27
FAST_SWITCH=17


GPIO.setmode(GPIO.BCM)
GPIO.setup(NERF_TRIGGER_1, GPIO.OUT)
GPIO.setup(NERF_TRIGGER_2, GPIO.OUT)
GPIO.setup(NERF_TRIGGER_RETURN, GPIO.IN)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SLOW_SWITCH, GPIO.OUT)
GPIO.setup(FAST_SWITCH, GPIO.OUT)
GPIO.output(SLOW_SWITCH, False)
GPIO.output(FAST_SWITCH, False)


def shoot(n_bullets):
    GPIO.output(NERF_TRIGGER_1, True)
    GPIO.output(NERF_TRIGGER_2, False)

    for i in range(n_bullets):
        print('spin')
        while GPIO.input(NERF_TRIGGER_RETURN) != 0:
            time.sleep(0.05)

        while GPIO.input(NERF_TRIGGER_RETURN) != 1:
            time.sleep(0.05)

    print('brake')

    GPIO.output(NERF_TRIGGER_1, False)
    GPIO.output(NERF_TRIGGER_2, True)
    time.sleep(0.02)

    GPIO.output(NERF_TRIGGER_1, True)
    GPIO.output(NERF_TRIGGER_2, True)

    time.sleep(0.3)

    if GPIO.input(NERF_TRIGGER_RETURN) == 0:
        print('spin')
        GPIO.output(NERF_TRIGGER_1, False)
        GPIO.output(NERF_TRIGGER_2, True)

        while GPIO.input(NERF_TRIGGER_RETURN) != 1:
            time.sleep(0.05)

        print('brake')
        GPIO.output(NERF_TRIGGER_1, False)
        GPIO.output(NERF_TRIGGER_2, False)

while True:
    print('SLOW')
    GPIO.output(FAST_SWITCH, False)
    GPIO.output(SLOW_SWITCH, True)
    time.sleep(2)
    print('FAST')
    GPIO.output(FAST_SWITCH, True)
    time.sleep(0.5)
    shoot(int(sys.argv[1]))
    GPIO.output(FAST_SWITCH, False)
    GPIO.output(SLOW_SWITCH, False)
    time.sleep(1)
