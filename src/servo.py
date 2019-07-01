#!/usr/bin/env python3
 
import time

try:
    import RPi.GPIO as GPIO

    class Servo(object):
        frequency = 50
        base_duty = 12.5
    
        def __init__(self, channel):
            self.channel = channel
        
        def start(self):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.channel, GPIO.OUT)
            self._servo = GPIO.PWM(self.channel, Servo.frequency)
            self._servo.start(Servo.base_duty)
    
        def do_cycle(self, cycle_duty):
            self._servo.ChangeDutyCycle(cycle_duty)
            time.sleep(1.0)
    
        def clean(self):
            self._servo.stop()
            GPIO.cleanup()
 
except RuntimeError:
    import sys
    print("It looks like we are not running on Raspberry Pi. The Servo class will therefore do nothing.", file=sys.stderr)
    
    class Servo(object):

        def __init__(self, channel):
            self.channel = channel
            
        def start(self):
            pass
        
        def do_cycle(self, cycle_duty):
            print("The Servo class is pretending to be spinning", file=sys.stderr)
        
        def clean(self):
            pass
        
