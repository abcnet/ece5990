import getopt
import socket
import sys


import subprocess
import sys
import os
import time
import threading


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
# pulses=[no,no]
# directions = [0, 0]
# d=['STOP','STOP']
# hist1=['STOP', 'STOP', 'STOP']
# hist2=['STOP', 'STOP', 'STOP']
# def drive_servo(servo_number, direction):
#     if servo_number==1:
#         p=p1
#     elif servo_number==2:
#         p=p2
#     else:
#         print "error"
#         return
#     if direction==0:
#         p.stop()
#     elif direction<0:
#         p.start(ccw/(20+ccw)*100.0)
#         p.ChangeFrequency(1000.0/(20+ccw))
#         # p.ChangeDutyCycle(1.7/21.7)
#     elif direction>0:
#         p.start(cw/(20+cw)*100.0)
#         p.ChangeFrequency(1000.0/(20+cw))
#         # p.ChangeDutyCycle(1.3/21.3)
#     else:
#         print "error"

# def drive(l,r,t):
#     if kill:
#         sys.exit("Quitting Program")
#     drive_servo(1, l)
#     drive_servo(2, r)
#     while t>0:
#         if kill:
#             sys.exit("Quitting Program")
#         time.sleep(1)
#         if not panic:
#             t -= 1
#     drive_servo(1, 0)
#     drive_servo(2, 0)



host = "0.0.0.0"
port = 8765

DEBUG = True

# Instead, you can pass command-line arguments
# -h/--host [IP] -p/--port [PORT]
# to put your server on a different IP/port.

from threading import Thread, Lock, Condition, Semaphore
from datetime import datetime
from shutil import copyfile

from test1 import postIP

nthreads = 2
# backupGroup = 32
IDLE = 0
AFTER_HELO = 1
AFTER_FROM = 2
AFTER_TO = 3
AFTER_DATA = 4

TIMEOUT = 10.0

DEBUG = True

def executeCommand(command):
    # print command
    try:
        if ON_RPI:
            l = eval(command[0])
            if l < -1:
                l = -1
            elif l > 1:
                l = 1
            if -0.01 < l < 0.01:
                p1.stop()
            else:
                dc = no + l * 0.2
                p1.start(dc/(20+dc)*100.0)
                p1.ChangeFrequency(1000.0/(20+dc))
            r = eval(command[1])
            if r < -1:
                r = -1
            elif r > 1:
                r = 1
            if -0.01 < r < 0.01:
                p2.stop()
            else:
                dc = no + r * 0.2
                p2.start(dc/(20+dc)*100.0)
                p2.ChangeFrequency(1000.0/(20+dc))

        t = eval(command[2])
        while t > 0:
            time.sleep(1)
            t -= 1
        if ON_RPI:
            p1.stop()
            p2.stop()
        return True
    except Exception as e:
        print e
        return False



# def checkCommand(l):
#     # print l
#     if len(l)<1:
#         return ILLEGAL, 0
#     first = l[0].upper()
#     if first == 'HELO':
#         return HELO, 0
#     if first == 'DATA':
#         return DATA, 0
#     if len(l)<2:
#         return ILLEGAL, 0
#     second = l[1].upper()
#     if first == 'MAIL':
#         if second == 'FROM:':
#             return MAIL_FROM, 0
#         if len(l)>=3 and l[2]==':':
#             return MAIL_FROM, 1
#         if second[:5] == 'FROM:' and len(second) > 5:
#             tmp = l[1][5:]
#             l[1:2] = ['FROM:', tmp]
#             return MAIL_FROM, 0
#     if first == 'RCPT':
#         if second == 'TO:':
#             return RCPT_TO, 0
#         if len(l)>=3 and l[2]==':':
#             return RCPT_TO, 1
#         if second[:3] == 'TO:' and len(second) > 3:
#             tmp = l[1][3:]
#             l[1:2] = ['TO:', tmp]
#             return RCPT_TO, 0
#     return ILLEGAL, 0

# f = open('mailbox', 'w')

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
        state = IDLE
        self.socket.send("From RPi server: connected\r\n")
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
                    # collect TCP stream until <CR><LF> is reached
                    stringbuffer += self.socket.recv(16)
                    timenow = datetime.now()
                    # calculate new timeout time
                    elapsed = (timenow - starttime).total_seconds()
                    if elapsed>=TIMEOUT:
                        self.socket.send('From RPi server Error: timeout exceeded\r\n')
                        self.socket.close()
                        return
                    else:
                        self.socket.settimeout(TIMEOUT - elapsed)
                if DEBUG:
                    print stringbuffer
                index = stringbuffer.find('\r\n')
                commandstring = stringbuffer[:index]
                if DEBUG:
                    print 'received', commandstring
                command = commandstring.split()
                stringbuffer = stringbuffer[index+2:]
                success = executeCommand(command)
                if success:
                    
                    self.socket.send("Success %s\r\n" % commandstring)
                    if DEBUG:
                        print 'Sent "Success %s\\r\\n" to iPhone' % commandstring
                    self.socket.settimeout(TIMEOUT)
                else:
                    
                    self.socket.send("Failed %s\r\n" % commandstring)
                    if DEBUG:
                        print 'Sent "Failed %s\\r\\n" to iPhone' % commandstring
                    self.socket.settimeout(TIMEOUT)
                self.socket.close()
                return
                # c, c2 = checkCommand(command)
                # if state != AFTER_DATA and c == ILLEGAL:
                #     # illegal command
                #     self.socket.send('502 5.5.2 Error: command not recognized\r\n')
                # elif state == IDLE:
                #     if c!=HELO:
                #         self.socket.send('503 Error: need HELO command\r\n')
                #     else:
                #         if len(command)<2:
                #             self.socket.send('501 Syntax: HELO yourhostname\r\n')
                #         elif len(command)>2:
                #             self.socket.send('501 Syntax: Space found in hostname after HELO\r\n')
                #         else:
                #             clientname = command[1]
                #             state = AFTER_HELO
                #             # state transitioned to AFTER_HELO
                #             self.socket.send("250 zr54\r\n")
                #             self.socket.settimeout(TIMEOUT)
                #             starttime = datetime.now()
                # elif state == AFTER_HELO:
                #     if c == HELO:
                #         self.socket.send('503 Error: duplicate HELO\r\n')
                #     elif c != MAIL_FROM:
                #         self.socket.send('503 Error: need MAIL FROM command\r\n')
                #     else:
                #         if len(command) < 3 + c2:
                #             self.socket.send('501 Syntax: MAIL FROM <email address>\r\n')
                #         elif len(command) > 3 + c2:
                #             i = commandstring.find(command[2+c2], commandstring.find(':')+2)
                #             badEmail = commandstring[i:]
                #             self.socket.send('504 5.5.2 <%s>: Sender address rejected\r\n' % badEmail)
                #         else:
                #             sender = command[2+c2]
                #             state = AFTER_FROM
                #             # state transitioned to AFTER_FROM
                #             self.socket.send('250 2.1.0 OK\r\n')
                #             self.socket.settimeout(TIMEOUT)
                #             starttime = datetime.now()
                # elif state == AFTER_FROM:
                #     if c == MAIL_FROM:
                #         self.socket.send('503 5.5.1 Error: nested MAIL command\r\n')
                #     elif c != RCPT_TO:
                #         self.socket.send('503 Error: need RCPT TO command\r\n')
                #     else:
                #         if len(command) < 3 + c2:
                #             self.socket.send('501 Syntax: RCPT TO <email address>\r\n')
                #         elif len(command) > 3 + c2:
                #             i = commandstring.find(command[2+c2], commandstring.find(':')+2)
                #             badEmail = commandstring[i:]
                #             self.socket.send('504 5.5.2 <%s>: Recipient address invalid\r\n' % badEmail)
                #         else:
                #             recipients.append(command[2+c2])
                #             state = AFTER_TO
                #             # state transitions to AFTER_TO
                #             self.socket.send('250 2.1.5 OK\r\n')
                #             self.socket.settimeout(TIMEOUT)
                #             starttime = datetime.now()
                # elif state == AFTER_TO:
                #     if c == RCPT_TO:
                #         if len(command) < 3 + c2:
                #             self.socket.send('501 Syntax: RCPT TO <email address>\r\n')
                #         elif len(command) > 3 + c2:
                #             i = commandstring.find(command[2+c2], commandstring.find(':')+2)
                #             badEmail = commandstring[i:]
                #             self.socket.send('504 5.5.2 <%s>: Recipient address invalid\r\n' % badEmail)
                #         else:
                #             recipients.append(command[2+c2])
                #             # state is still AFTER_TO
                #             self.socket.send('250 2.1.5 OK\r\n')
                #             self.socket.settimeout(TIMEOUT)
                #             starttime = datetime.now()
                #     elif c != DATA:
                #         self.socket.send('503 Error: need DATA or RCPT TO command\r\n')
                #     else:
                #         if len(command)>1:
                #             self.socket.send('501 Syntax: No argument allowed for DATA\r\n')
                #         else:
                #             state = AFTER_DATA
                #             # state transitions to AFTER_DATA
                #             self.socket.send("354 End data with <CR><LF>.<CR><LF>\r\n")
                #             self.socket.settimeout(TIMEOUT)
                #             starttime = datetime.now()
                # elif state == AFTER_DATA:
                #     if commandstring == '.':
                #         with ConnectionHandler.lock:
                #             while ConnectionHandler.locked:
                #                 ConnectionHandler.cond.wait()
                #             ConnectionHandler.locked = True
                #             ConnectionHandler.count += 1
                #             tmpcount = ConnectionHandler.count
                           
                #             ConnectionHandler.locked = False
                #             ConnectionHandler.cond.notify()
                #         self.socket.send("250 OK: delivered message %d\r\n" % tmpcount)
                #         state = AFTER_HELO
                #         self.socket.settimeout(TIMEOUT)
                #         starttime = datetime.now()
                #         recipients = []
                #         data = []
                #     else:
                #         data.append(commandstring)

            except socket.timeout:
                self.socket.send('From RPi server Error: timeout exceeded\r\n')
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

    def serverloop_singlethread():

        while True:
            # accept a connection
            (clientsocket, address) = serversocket.accept()
            ct = ConnectionHandler(clientsocket)
            ct.handle()

    for i in range(nthreads):
        # print('Running thread %d' % i)
        thread = Thread(target=serverloop_singlethread)
        thread.start()

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
