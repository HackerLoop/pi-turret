#!/usr/bin/python2.7

import websocket
import thread
import time
import picamera

import json

from servos import Servos

### Confs

SERVO_I2C_ADDRESS 	= 0x40		# I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL = 0 		# Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL = 1			# Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ 		= 50 		# PWM frequency for the servos in HZ (should be 50)
SERVO_MIN 			= 150		# Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX 			= 650		# Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER		= 400		# Center value for the servo, should be 0 degrees of rotation.

synced = False

### utils

def _reset_servos():
    s.setXAxis(350)
    s.setYAxis(350)

### code

s = Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)
_reset_servos()

camera = picamera.PiCamera()

def on_orientation(data):
    if synced == False:
	return
    x = -data[1]['orientation']['z']
    y = data[1]['orientation']['y']

    span = 650 - 150
    s.setXAxis(int(350 + x * span / 2))
    s.setYAxis(int(350 + y * span / 2))

    #print('{0:.6f} {1:.6f}'.format(x, y))

def on_pose(data): 
    print(data)

def on_arm_unsynced(data):
    print('unsynced')
    global synced
    synced = False
    _reset_servos()

def on_arm_synced(data):
    print('synced')
    global synced
    synced = True

def on_message(ws, message):
    #print(message)
    data = json.loads(message)
    myo_cmds = {"orientation" : on_orientation, "pose" : on_pose, "arm_unsynced" : on_arm_unsynced, "arm_synced" : on_arm_synced}

    event = data[1]['type']
    if not event in myo_cmds:
	print('{0} not found'.format(event))
	return

    myo_cmd = myo_cmds[event]
    myo_cmd(data)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    s.setXAxis(400)
    s.setYAxis(400)
    pass

if __name__ == "__main__":
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://192.168.1.15:10139/myo/2", 
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
