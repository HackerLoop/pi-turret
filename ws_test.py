#!/bin/env python2.7

import websocket
import thread
import time

import json

from servos import Servos

SERVO_I2C_ADDRESS 	= 0x40		# I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL = 0 		# Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL = 1			# Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ 		= 50 		# PWM frequency for the servos in HZ (should be 50)
SERVO_MIN 			= 150		# Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX 			= 650		# Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER		= 400		# Center value for the servo, should be 0 degrees of rotation.



s = servos.Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)

def on_message(ws, message):
    data = json.loads(message)
    x = data[1]['accelerometer'][0]
    y = data[1]['accelerometer'][1]

    span = 650 - 150
    s.setXAxis(150 + x * span / 2)
    s.setXAxis(150 + y * span / 2)

    print('{0:.6f} {1:.6f}'.format(x, y))

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    pass

if __name__ == "__main__":
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://192.168.1.15:10139/myo/2", 
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
