#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import numpy as np
from bluepy.btle import Scanner, DefaultDelegate

# Setup
GPIO.setmode(GPIO.BCM)
pinList = [18, 23]
beaconList = [["d6:2b:0f:86:85:e9", "Beacon verde"]]
SleepTimeL = 1
activeBeacons = []
distance = 60

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)


# Classes
class ActiveBeacon:
    def __init__(self, beaconMac = "", beaconName = "", rssi = -999):
        self.addr = beaconMac
        self.name = beaconName
        self.bufferRSSI = [-999, -999, -999, -999, -999]


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            addActiveBeacon(dev.addr, dev.rssi)
            #print "Discovered device %s: %s" % (getBeaconName(dev.addr), dev.addr)

        if isAnActiveBeacon(dev.addr):
            for b in activeBeacons:
                if b.addr == dev.addr.lower():
                    # Actualizamos el ultimo RSSI del beacon
                    b.bufferRSSI[-1] = dev.rssi
                    if abs(b.bufferRSSI[-1]) <= distance:
                        switchRelaysOn()
                    break
            print "Device = %s, RSSI = %d dB, count = %i" % (dev.addr, dev.rssi, dev.updateCount)

def addActiveBeacon(addr, rssi):
    if not isAnActiveBeacon(addr):
        if isARegisteredBeacon(addr):
            activeBeacons.append(ActiveBeacon(addr, getBeaconName(addr), rssi))


def isARegisteredBeacon(addr):
    for b in beaconList:
        if b[0] == addr.lower():
            return True
    return False

def isAnActiveBeacon(addr):
    for b in activeBeacons:
        if b.addr == addr.lower():
            return True
    return False

def getBeaconName(addr):
    for b in beaconList:
        if b[0] == addr.lower():
            return b[1]
    return "Not registered"

def switchRelaysOn():
    for i in pinList:
        GPIO.output(i, GPIO.LOW)

def switchRelaysOff():
    for i in pinList:
        GPIO.output(i, GPIO.HIGH)



# Code

try:
    GPIO.output(18, GPIO.LOW)
    print "ONE"
    time.sleep(SleepTimeL);
    GPIO.output(23, GPIO.LOW)
    print "TWO"
    time.sleep(SleepTimeL);
    #GPIO.cleanup()

    print "Starting BLE scan"
    #p = btle.Peripheral("d6:2b:0f:86:85:e9", "random")
    scanner = Scanner().withDelegate(ScanDelegate())
    scanner.start()

    while True:
        #print "Still running..."
        #scanner.clear()
        print '--------'
        powerRelays = False
        for b in activeBeacons:
            print "%s, %s, %d, %d, %d, %d, %d, %d" % (b.addr, b.name, len(b.bufferRSSI), b.bufferRSSI[0], b.bufferRSSI[1], b.bufferRSSI[2], b.bufferRSSI[3], b.bufferRSSI[4])

            for i in b.bufferRSSI:
                if abs(i) < distance:
                    powerRelays = True

            del b.bufferRSSI[0]
            b.bufferRSSI.append(-999)

        if not powerRelays:
            switchRelaysOff()
            print "Power off"
        else:
            print "Power on"

        print '--------'
        scanner.process(1.0)
    # devices = scanner.scan(10.0)
    #
    # for dev in devices:
    #     print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    #     for (adtype, desc, value) in dev.getScanData():
    #         print "  %s = %s" % (desc, value)

    print "Good bye!"


except KeyboardInterrupt:
    print " Quit"
    GPIO.cleanup()
