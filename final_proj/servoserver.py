import getopt
import socket
import sys


import subprocess
import sys
import os
import time
import threading

import picamera

#initialize camera module
#camera = picamera.PiCamera()
#camera.resolution = (1280, 720)
#camera.framerate = 24
#camera.vflip = True
#camera.hflip = True


ON_RPI = False if sys.platform.find('darwin') > -1 else True
if ON_RPI:
    import RPi.GPIO as GPIO
    import picamera

# code for setting up two threads from http://stackoverflow.com/questions/6286235/terminate-multiple-threads-when-any-thread-completes-a-task

#setup touchscreen io
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
CHANNEL1 = 19
CHANNEL2 = 16
freq = 46.51
cw=1.3
no=1.5
ccw=1.7
if ON_RPI:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM) #Setforbroadcomnumberingnotboardnumbering

    # GPIO pin setup
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CHANNEL1, GPIO.OUT)
    GPIO.setup(CHANNEL2, GPIO.OUT)
    # GPIO.cleanup()




#define interrupt handlers
def GPIO17_callback(channel):
    GPIO.cleanup()
    sys.exit("Quitting Server")
if ON_RPI:
    #interrupt detection
    GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
    p1 = GPIO.PWM(CHANNEL1, freq)
    p2 = GPIO.PWM(CHANNEL2, freq)




host = "0.0.0.0"
port = 8765
port2 = 8766

DEBUG = True

# Instead, you can pass command-line arguments
# -h/--host [IP] -p/--port [PORT]
# to put your server on a different IP/port.

from threading import Thread, Lock, Condition, Semaphore
from datetime import datetime
from shutil import copyfile

from test1 import postIP

nthreads = 32
nthreads = 2
# backupGroup = 32
IDLE = 0
AFTER_HELO = 1
AFTER_FROM = 2
AFTER_TO = 3
AFTER_DATA = 4

TIMEOUT = 10000.0

DEBUG = True

left = 0
right = 0
timeleft = 0
iPhoneConnected = False

def iPhoneConnect():
    global iPhoneConnected
    if DEBUG:
        print "-----------iPhone connected---------"
    iPhoneConnected = True
def iPhoneDisconnect():
    global iPhoneConnected
    if DEBUG:
        print '------------iPhone DISCONNECTED-------'
    iPhoneConnected = False

def writeCommand(command):
    print 'writing command'
    global left
    global right
    global timeleft
    try:
        left = eval(command[0])
            
        right = eval(command[1])
           

        timeleft = eval(command[2])
        print 'done writing command'
        return True
    except Exception as e:
        print e
        return False

def executeCommand():
    global timeleft
    while True:
        if timeleft <= 0:
            if ON_RPI:
                p1.stop()
                p2.stop()
            time.sleep(0.1)
        if ON_RPI and timeleft > 0:
            l = left
            if l < -1:
                l = -1
            elif l > 1:
                l = 1
            if -0.01 < l < 0.01:
                p1.stop()
            elif timeleft > 0:
                dc = no + l * 0.2
                p1.start(dc/(20+dc)*100.0)
                p1.ChangeFrequency(1000.0/(20+dc))
            r = right
            if r < -1:
                r = -1
            elif r > 1:
                r = 1
            if -0.01 < r < 0.01:
                p2.stop()
            elif timeleft > 0:
                dc = no + r * 0.2
                p2.start(dc/(20+dc)*100.0)
                p2.ChangeFrequency(1000.0/(20+dc))
        if timeleft > 0:
            time.sleep(0.1)
            timeleft -= 0.1
        
def door(command):
    try:
        if command[0] == '1':
            pass

    except Exception as e:
        print e

class ConnectionHandler:
    """Handles a single client request"""
    count = 0
    lock = Lock()
    locked = False
    cond = Condition(lock)

    def __init__(self, socket):
        self.socket = socket

    def handle(self):
        # global f
        # state = IDLE
        # self.socket.send("From RPi server: connected\r\n")
        iPhoneConnect()
        self.socket.settimeout(TIMEOUT)
        starttime = datetime.now()
        stringbuffer = ''
        clientname = ''
        sender = ''
        recipients = []
        data = []
        while True:
            try:
                while stringbuffer.find('\r\n')==-1:
                    # print 'cannot find \\r\\n'
                    # collect TCP stream until <CR><LF> is reached
                    # print stringbuffer
                    stringbuffer += self.socket.recv(16)
                    # print 'timenow'
                    timenow = datetime.now()
                    # calculate new timeout time
                    elapsed = (timenow - starttime).total_seconds()
                    # print 'elpased'
                    if elapsed>=TIMEOUT:
                        # self.socket.send('From RPi server Error: timeout exceeded\r\n')
                        self.socket.close()
                        return
                    else:
                        self.socket.settimeout(TIMEOUT - elapsed)
                    # print 'end of inner while'
                if DEBUG:
                    print stringbuffer
                index = stringbuffer.find('\r\n')
                commandstring = stringbuffer[:index]
                if DEBUG:
                    print 'received', commandstring
                command = commandstring.split()
                stringbuffer = stringbuffer[index+2:]

                

                success = writeCommand(command)
                print 'about to send received'
                self.socket.send("Received %s\r\n" % commandstring)
                print 'received sent'
                self.socket.settimeout(TIMEOUT)
                # if success:
                    
                #     self.socket.send("Success %s\r\n" % commandstring)
                #     if DEBUG:
                #         print 'Sent "Success %s\\r\\n" to iPhone' % commandstring
                #     self.socket.settimeout(TIMEOUT)
                # else:
                    
                #     self.socket.send("Failed %s\r\n" % commandstring)
                #     if DEBUG:
                #         print 'Sent "Failed %s\\r\\n" to iPhone' % commandstring
                #     self.socket.settimeout(TIMEOUT)
                # self.socket.close()
                # return
               

            except socket.timeout:
                # self.socket.send('From RPi server Error: timeout exceeded\r\n')
                self.socket.close()
                iPhoneDisconnect()
                return
            except socket.error as e:
                print e
                self.socket.close()
                iPhoneDisconnect()
                return

class ConnectionHandler2:
    """Handles a single client request"""
    count = 0
    lock = Lock()
    locked = False
    cond = Condition(lock)

    def __init__(self, socket):
        self.socket = socket

    def handle2(self):
        # global f
        # state = IDLE
        # self.socket.send("From RPi server: connected\r\n")
        self.socket.settimeout(TIMEOUT)
        starttime = datetime.now()
        stringbuffer = ''
        clientname = ''
        sender = ''
        recipients = []
        data = []
        while True:
            try:
                while stringbuffer.find('\r\n')==-1:
                    # print 'cannot find \\r\\n'
                    # collect TCP stream until <CR><LF> is reached
                    # print stringbuffer
                    stringbuffer += self.socket.recv(16)
                    # print 'timenow'
                    timenow = datetime.now()
                    # calculate new timeout time
                    elapsed = (timenow - starttime).total_seconds()
                    # print 'elpased'
                    if elapsed>=TIMEOUT:
                        # self.socket.send('From RPi server Error: timeout exceeded\r\n')
                        self.socket.close()
                        return
                    else:
                        self.socket.settimeout(TIMEOUT - elapsed)
                    # print 'end of inner while'
                if DEBUG:
                    print stringbuffer
                index = stringbuffer.find('\r\n')
                commandstring = stringbuffer[:index]
                if DEBUG:
                    print 'Wifi Thread: ', commandstring
                command = commandstring.split()
                stringbuffer = stringbuffer[index+2:]



                

                # success = 
                print 'Wifi Thread: about to send received'
                self.socket.send("Received %s\r\n" % commandstring)
                print 'Wifi Thread: received sent'
                self.socket.settimeout(TIMEOUT)
                # if success:
                    
                #     self.socket.send("Success %s\r\n" % commandstring)
                #     if DEBUG:
                #         print 'Sent "Success %s\\r\\n" to iPhone' % commandstring
                #     self.socket.settimeout(TIMEOUT)
                # else:
                    
                #     self.socket.send("Failed %s\r\n" % commandstring)
                #     if DEBUG:
                #         print 'Sent "Failed %s\\r\\n" to iPhone' % commandstring
                #     self.socket.settimeout(TIMEOUT)
                # self.socket.close()
                # return
               

            except socket.timeout:
                # self.socket.send('From RPi server Error: timeout exceeded\r\n')
                self.socket.close()
                return
            except socket.error as e:
                print e
                self.socket.close()
                return

def serverloop():
    """The main server loop"""

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # mark the socket so we can rebind quickly to this port number
    # after the socket is closed
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the local loopback IP address and special port
    serversocket.bind((host, port))
    # start listening with a backlog of 5 connections
    serversocket.listen(5)


    serversocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # mark the socket so we can rebind quickly to this port number
    # after the socket is closed
    serversocket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind the socket to the local loopback IP address and special port
    serversocket2.bind((host, port2))
    # start listening with a backlog of 5 connections
    serversocket2.listen(5)

    def serverloop_singlethread():

        while True:
            # accept a connection
            (clientsocket, address) = serversocket.accept()
            ct = ConnectionHandler(clientsocket)
            ct.handle()

    def serverloop_singlethread2():

        while True:
            # accept a connection
            (clientsocket2, address2) = serversocket2.accept()
            ct2 = ConnectionHandler2(clientsocket2)
            ct2.handle2()

    for i in range(nthreads):
        # print('Running thread %d' % i)
        thread = Thread(target=serverloop_singlethread)
        thread.start()

    servoThread = Thread(target=executeCommand)
    servoThread.start()

    wifiThread = Thread(target=serverloop_singlethread2)
    wifiThread.start()

if __name__ == '__main__':
    if DEBUG:
        print 'posting IP to firebase...'
    postIP()

    opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ['host=', 'port='])

    for k, v in opts:
        if k in ('-h', '--host'):
            host = v
        if k in ('-p', '--port'):
            port = int(v)

    print("Server coming up on %s:%i" % (host, port))
    serverloop()
