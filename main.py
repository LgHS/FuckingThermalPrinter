#!/usr/bin/env python
# coding: utf-8

''' I'm sorry for this, please don't judge me ... '''

import struct
import time
import serial
import requests
import os

class FuckingThermalPrinter(object):
    SERIALPORT          = '/dev/ttyAMA0'
    BAUDRATE            = 19200
    TIMEOUT             = 3
    _ESC                = chr(27)
    printer             = None

    def __init__(self, serialport=SERIALPORT):
        self.printer = serial.Serial(serialport, self.BAUDRATE, timeout=self.TIMEOUT)
        self.printer.write(self._ESC)   # ESC - command
        self.printer.write(chr(64))     # @   - initialize
        self.printer.write(self._ESC)   # ESC - command
        self.printer.write(chr(55))     # 7   - print settings
        self.printer.write(chr(7))      # Heating dots (20=balance of darkness vs no jams) default = 20
        self.printer.write(chr(80))     # heatTime Library default = 255 (max)
        self.printer.write(chr(2))      # Heat interval (500 uS = slower, but darker) default = 250
        printDensity = 15               # 120% (? can go higher, text is darker but fuzzy)
        printBreakTime = 15             # 500 uS
        self.printer.write(chr(18))
        self.printer.write(chr(35))
        self.printer.write(chr((printDensity << 4) | printBreakTime))

    def linefeed(self, number=1):
        for _ in range(number):
            self.printer.write(chr(10))

    def print_text(self, msg, chars_per_line=None):
        self.printer.write(msg)
        time.sleep(0.2)

    def show_entry(self, timestamp, id_name, name, action):
        p.print_text(timestamp)
        p.linefeed(number=1)
        p.print_text("id:" + id_name)
        p.linefeed(number=1)
        p.print_text("name:" + name)
        p.linefeed(number=1)
        p.print_text("profil picture: [Censured]")
        p.linefeed(number=1)
        p.print_text("action:" + action)
        p.linefeed(number=2)
    
if __name__ == '__main__':
    # Init
    p = FuckingThermalPrinter()
    p.linefeed(number=1)
    # Header
    p.print_text("#cat /var/log/lghs.facebook.log")
    p.linefeed(number=1)
    while 42:
        # Get info
        r = requests.get('https://facebook.lghs.space/thermal')
        data = r.json()
        # Print info
        for entry in data:
            p.show_entry(entry[u'timestamp'], entry[u'sender_id'], entry[u'name'], entry[u'action'])
            time.sleep(2)
        time.sleep(5)
