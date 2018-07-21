#!/usr/bin/env python3
 
import RPi.GPIO as GPIO
import time

class Servo(object):
    frequency = 50
    base_duty = 7.5

    def __init__(self, channel):
        self.channel = channel
    
    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.OUT)
        self._servo = GPIO.PWM(self.channel, Servo.frequency)
        self._servo.start(Servo.base_duty)

    def do_cycle(self,cycle_duty):
        self._servo.ChangeDutyCycle(cycle_duty)
        time.sleep(1.0)

    def clean(self):
        self._servo.stop()
        GPIO.cleanup()
 
if __name__ == '__main__':
    servo = Servo(18)
    servo.start()

    base_duty = 7.5
    base_delta_duty = 5
    servo.do_cycle(base_duty - base_delta_duty)
    servo.do_cycle(base_duty + 2. * base_delta_duty)
    servo.do_cycle(base_duty - base_delta_duty)

    servo.clean()

