#!/bin/env python

import signal
import sys

import time

from trigger import Trigger

trigger = Trigger()

def signal_handler(signal, frame):
    trigger.reset()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

trigger.pre_shoot()

n_bullets = int(sys.argv[1])
while True:
    trigger.shoot(n_bullets)
    time.sleep(1 * n_bullets)
