#!/usr/bin/python
#well, this script scans for bluetooth devices (MAC ADDRESSES)
#if the bluetooth device is found then the device is at home(in range)


import bluetooth
import time
import sys

print "In/Out Board"

while True:
    print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

    result = bluetooth.lookup_name('0C:30:21:41:E7:18', timeout=5)
    if (result != None):
        print "Sandy: in"
    else:
        print "Sandy: out"

    result = bluetooth.lookup_name('F0:DB:F8:5C:60:D1', timeout=5)
    if (result != None):
        print "Assel: in"
    else:
        print "Assel: out"

    result = bluetooth.lookup_name('BC:6C:21:31:59:A8', timeout=5)
    if (result != None):
        print "Derik: in"
    else:
        print "Derik: out"


    time.sleep(1)
