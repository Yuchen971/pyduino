#!/usr/bin/python
import fcntl, serial
import serial
import time
import numpy as np
import sys
from serial import tools
from serial.tools import list_ports
#from phant import Phant
#In [36]: serial.tools.list_ports.comports()[0][0]
#Out[36]: '/dev/ttyUSB0'
#
#In [37]: serial.tools.list_ports.comports()[0][1]
#Out[37]: 'FT231X USB UART'
#
#In [38]: serial.tools.list_ports.comports()[0][2]
#Out[38]: 'USB VID:PID=0403:6015 SER=DN01J0PU LOCATION=6-2'
# i think here requires a bit more
#tty=serial.tools.list_ports.comports()[0]

def open_port(portname):
    ### this script is for the purpose of locking the port when it is  used by other script
    ### following http://stackoverflow.com/questions/19809867/how-to-check-if-serial-port-is-already-open-by-another-process-in-linux-using
    ### and http://arduino.stackexchange.com/questions/36621/allow-only-one-serial-connection-using-pyserial?noredirect=1#comment73104_36621
    tty_found=False
    for tty_list in serial.tools.list_ports.comports():
        if portname==tty_list[2][:len(portname)]:
           tty=tty_list
           tty_found=True
           break

    if tty_found:
        # trying to open up the port
        try:
            port = serial.Serial(port=tty[0]) #,9600,timeout=None)
            if port.isOpen():
                try:
                    fcntl.flock(port.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return [True,port]
                except IOError:
                    print 'Port {0} is busy'.format(tty)
                    return [False,[]]
                #else:
                #    yield port
        except serial.SerialException as ex:
            print 'Port {0} is unavailable: {1}'.format(tty, ex)
            return [False,[]]
    else: 
        print 'Port '+portname+' is not found'
        return [False,[]]
