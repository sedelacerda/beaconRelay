#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pinList = [18, 23]


for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

SleepTimeL = 1

try:
    GPIO.output(18, GPIO.LOW)
    print "ONE"
    time.sleep(SleepTimeL);
    GPIO.output(23, GPIO.LOW)
    print "TWO"
    time.sleep(SleepTimeL);
    GPIO.cleanup()
    print "Good bye!"

except KeyboardInterrupt:
    print " Quit"
    GPIO.cleanup()
