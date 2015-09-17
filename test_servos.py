#!/bin/env python

import time
import signal

import math

from servos import Servos

SERVO_I2C_ADDRESS	= 0x40		# I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL = 0			# Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL = 1			# Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ		= 50		# PWM frequency for the servos in HZ (should be 50)
SERVO_MIN			= 250		# Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX			= 430		# Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER		= 340		# Center value for the servo, should be 0 degrees of rotation.

s = Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)

def signal_handler(signal, frame):
    s.setXAxis(SERVO_CENTER)
    s.setYAxis(SERVO_CENTER)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

s.setXAxis(SERVO_CENTER)
s.setYAxis(SERVO_CENTER)

SPAN_MIN = SERVO_CENTER - SERVO_MIN
SPAN_MAX = SERVO_MAX - SERVO_CENTER
for i in range(0, 10000000):
    deg = i / 360.0 * math.pi
    cos = math.cos(deg)
    sin = math.sin(deg)
    span_x = SPAN_MIN if cos < 0 else SPAN_MAX
    span_y = SPAN_MIN if sin < 0 else SPAN_MAX
    x = SERVO_CENTER + int(cos * span_x)
    y = SERVO_CENTER + int(sin * span_y)
    s.setXAxis(x)
    s.setYAxis(y)
    print('x: {0} y: {1}'.format(x, y))
    time.sleep(0.01)

s.setXAxis(SERVO_CENTER)
s.setYAxis(SERVO_CENTER)
