#!/usr/bin/python
import fcntl, serial
import serial
import time
import numpy as np
import sys
from serial import tools
from serial.tools import list_ports #from phant import Phant
import pdb
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

def open_port(portname,time_out,sw_match_existing):
    ### this script is for the purpose of locking the port when it is  used by other script
    ### following http://stackoverflow.com/questions/19809867/how-to-check-if-serial-port-is-already-open-by-another-process-in-linux-using
    ### and http://arduino.stackexchange.com/questions/36621/allow-only-one-serial-connection-using-pyserial?noredirect=1#comment73104_36621
    tty_found=False
    for tty_list in serial.tools.list_ports.comports():
        if portname==tty_list[2][:len(portname)]:
           tty=tty_list[0]
           tty_found=True
           break
    if not sw_match_existing:tty= portname

    if tty_found or not sw_match_existing:
        # trying to open up the port
        try:
            #port = serial.Serial(port=tty[0]) #,9600,timeout=None)
            #port = serial.Serial(port=tty[0],9600,timeout=None)
            #pdb.set_trace()
            port = serial.Serial(port=tty,baudrate=9600,timeout=time_out)
            if port.isOpen():
                try:
                    fcntl.flock(port.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    time.sleep(3) #critical
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

def close_port(portname):
    portname.close()
    return False

def initialize(device_handle):
### this script is to make sure that arduino is ready to return the result as expected
    initialized=False
    writing_string='abc'
    while initialized==False:
        device_handle.write(writing_string)
        time.sleep(2)
        if writing_string == device_handle.readline().rstrip():
            initialized=True

def list_devices():
    return serial.tools.list_ports.comports()

def get_result_by_input(**kwargs):
    ### match exisitng ports is to check whether the input port is exising

    arg_defaults = {
                'port':'port',
                'command':None,
                'initialize':True,
                'timeout':600,
                'match_existing_ports': True,
                   }
    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)

    [port_sensor_isopen, sensor_fid]=open_port(arg['port'],arg['timeout'],arg['match_existing_ports'])
    while port_sensor_isopen == False:
        [port_sensor_isopen, sensor_fid]=open_port(arg['port'],arg['timeout'],arg['match_existing_ports'])
        time.sleep(10)
    if arg['initialize']: initialize(sensor_fid)

    sensor_fid.write(arg['command'])
    msg = sensor_fid.readline()
    port_sensor_isopen=close_port(sensor_fid)
    return msg
