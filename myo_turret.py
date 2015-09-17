#!/bin/env python

import signal
import websocket
import thread
from threading import Timer
import time
import math
# import picamera

import json

from servos import Servos
from trigger import Trigger

### Confs

SERVO_I2C_ADDRESS       = 0x40          # I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL = 0                 # Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL = 1                 # Channel for the y axis rotation which controls laser left/right
SERVO_PWM_FREQ          = 50            # PWM frequency for the servos in HZ (should be 50)
SERVO_MIN                       = 170           # Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX                       = 480           # Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER            = 340           # Center value for the servo, should be 0 degrees of rotation.

synced = False

### utils

def _reset_servos():
    s.setXAxis(SERVO_CENTER)
    s.setYAxis(SERVO_CENTER)

### code

trigger = Trigger()

# servo driver conf
s = Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, SERVO_PWM_FREQ)
_reset_servos()

def signal_handler(signal, frame):
    _reset_servos()
    trigger.reset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# pi camera setup
# camera = picamera.PiCamera()


## myo websocket handlers

orientation = {'x' : 0, 'y' : 0}

def on_orientation(data):
    global orientation
    if synced == False:
        return

    def _filter_decimal(value):
        return float(int(value * 1000)) / 1000

    orientation_x = _filter_decimal(data[1]['gyroscope'][2] / 8000)
    orientation_y = _filter_decimal(data[1]['gyroscope'][1] / 5000)
    if math.fabs(orientation_x) >= 1 or math.fabs(orientation_y) >= 1:
        return

    x = min(max(orientation['x'] + orientation_x, -1), 1)
    y = min(max(orientation['y'] + orientation_y, -1), 1)
    orientation['x'] = x
    orientation['y'] = y

    # print('{0: <10} {1: <10}'.format(x, y))

    span = SERVO_MAX - SERVO_MIN
    s.setXAxis(int(SERVO_CENTER + x * span / 2))
    s.setYAxis(int(SERVO_CENTER + y * span / 2))

def on_pose(data): 
    global orientation
    if data[1]['pose'] == 'fist':
        trigger.shoot(1)
    if data[1]['pose'] in ('wave_in', 'wave_out'):
        print('reset zero position ####################################################################')
        orientation = {'x' : 0, 'y' : 0}
    print(data)

def on_locked(data):
    GPIO.output(NERF_TRIGGER, False)

def on_arm_unsynced(data):
    print('unsynced')
    global synced, orientation
    synced = False
    orientation = {'x' : 0, 'y' : 0}
    _reset_servos()
    trigger.reset()

def on_arm_synced(data):
    print('synced')
    global synced
    trigger.pre_shoot()
    synced = True

def on_message(ws, message):
    #print(message)
    data = json.loads(message)
    myo_cmds = {"orientation" : on_orientation, "pose" : on_pose, "arm_unsynced" : on_arm_unsynced, "arm_synced" : on_arm_synced, 'locked' : on_locked}

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
    global orientation
    orientation = {'x' : 0, 'y' : 0}
    s.setXAxis(SERVO_CENTER)
    s.setYAxis(SERVO_CENTER)
    pass

if __name__ == "__main__":
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("ws://192.168.2.1:10139/myo/3", 
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()
