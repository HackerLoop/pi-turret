#!/bin/env python

import time
import signal

import math

from servos import Servos

SERVO_I2C_ADDRESS	= 0x40		# I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL = 0			# Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL = 1			# Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ		= 50		# PWM frequency for the servos in HZ (should be 50)
SERVO_MIN			= 170		# Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX			= 480		# Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER		= 340		# Center value for the servo, should be 0 degrees of rotation.

s = Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)

def signal_handler(signal, frame):
    s.setXAxis(SERVO_CENTER)
    s.setYAxis(SERVO_CENTER)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

servo_span = SERVO_MAX - SERVO_MIN
for i in range(0, 10000):
    s.setXAxis(SERVO_MIN + int(math.cos(i / math.pi ) * servo_span))
    # s.setYAxis(i)
    print('i: {0}'.format(i))
    time.sleep(0.01)

s.setXAxis(SERVO_CENTER)
s.setYAxis(SERVO_CENTER)
