import time

import threading

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

class TriggerThread(threading.Thread):

    def __init__(self, trigger, n_bullets):
        super(TriggerThread, self).__init__()
        self.trigger = trigger
        self.n_bullets = n_bullets
        self.lock = threading.Lock()
        self.start()

    def run(self):
        self.shoot()
        self.trigger.end_shoot()

    def shoot(self):
        GPIO.output(NERF_TRIGGER_1, True)
        GPIO.output(NERF_TRIGGER_2, False)

        while True:
            print('spin')
            while GPIO.input(NERF_TRIGGER_RETURN) != 0:
                time.sleep(0.05)

            while GPIO.input(NERF_TRIGGER_RETURN) != 1:
                time.sleep(0.05)

            self.lock.acquire()
            self.n_bullets -= 1
            if self.n_bullets == 0:
                break
            self.lock.release()

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
            GPIO.output(NERF_TRIGGER_1, True)
            GPIO.output(NERF_TRIGGER_2, True)

    def add_bullets(self, n_bullets):
        self.lock.acquire()
        self.n_bullets += n_bullets
        self.lock.release()

    def get_bullets_left(self):
        n_bullets = 0
        self.lock.acquire()
        n_bullets = self.n_bullets
        self.lock.release()
        return n_bullets


class Trigger():

    def __init__(self):
        self.lock = threading.Lock()
        self.current_trigger_thread = None

    def reset(self):
        join = False
        self.lock.acquire()
        join = self.current_trigger_thread is not None
        self.lock.release()
        if join:
            self.current_trigger_thread.join()

        GPIO.output(SLOW_SWITCH, False)
        GPIO.output(FAST_SWITCH, False)
        GPIO.output(NERF_TRIGGER_1, True)
        GPIO.output(NERF_TRIGGER_2, True)

    def pre_shoot(self):
        GPIO.output(FAST_SWITCH, False)
        GPIO.output(SLOW_SWITCH, True)

    def sleep(self):
        GPIO.output(SLOW_SWITCH, False)
        GPIO.output(FAST_SWITCH, False)

    def shoot(self, n_bullets):
        self.lock.acquire()
        if self.current_trigger_thread is not None:
            self.current_trigger_thread.add_bullets(n_bullets)
        else:
            GPIO.output(FAST_SWITCH, True)
            self.current_trigger_thread = TriggerThread(self, n_bullets)
        self.lock.release()

    def end_shoot(self):
        self.lock.acquire()
        self.current_trigger_thread = None
        self.lock.release()
        self.pre_shoot()
        GPIO.output(FAST_SWITCH, False)

    def get_bullets_left(self):
        n_bullets = 0
        self.lock.acquire()
        if self.current_trigger_thread is not None:
            n_bullets = self.current_trigger_thread.get_bullets_left()
        self.lock.release()
        return n_bullets
