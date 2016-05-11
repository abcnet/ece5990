import getopt
import socket
import sys



host = "255.255.255.255"
port = 8765
# Instead, you can pass command-line arguments
# -h/--host [IP] -p/--port [PORT]
# to put your server on a different IP/port.

from threading import Thread, Lock, Condition, Semaphore
from datetime import datetime
from shutil import copyfile

nthreads = 32
backupGroup = 32
IDLE = 0
AFTER_HELO = 1
AFTER_FROM = 2
AFTER_TO = 3
AFTER_DATA = 4

TIMEOUT = 10.0

HELO = 0
MAIL_FROM = 1
RCPT_TO = 2
DATA = 3
ILLEGAL = -1

def checkCommand(l):
    # print l
    if len(l)<1:
        return ILLEGAL, 0
    first = l[0].upper()
    if first == 'HELO':
        return HELO, 0
    if first == 'DATA':
        return DATA, 0
    if len(l)<2:
        return ILLEGAL, 0
    second = l[1].upper()
    if first == 'MAIL':
        if second == 'FROM:':
            return MAIL_FROM, 0
        if len(l)>=3 and l[2]==':':
            return MAIL_FROM, 1
        if second[:5] == 'FROM:' and len(second) > 5:
            tmp = l[1][5:]
            l[1:2] = ['FROM:', tmp]
            return MAIL_FROM, 0
    if first == 'RCPT':
        if second == 'TO:':
            return RCPT_TO, 0
        if len(l)>=3 and l[2]==':':
            return RCPT_TO, 1
        if second[:3] == 'TO:' and len(second) > 3:
            tmp = l[1][3:]
            l[1:2] = ['TO:', tmp]
            return RCPT_TO, 0
    return ILLEGAL, 0

f = open('mailbox', 'w')

class ConnectionHandler:
    """Handles a single client request"""
    count = 0
    lock = Lock()
    locked = False
    cond = Condition(lock)

    def __init__(self, socket):
        self.socket = socket

    def handle(self):
        global f
        state = IDLE
        self.socket.send("220 zr54 SMTP CS4410MP3\r\n")
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
                        self.socket.send('421 4.4.2 zr54 Error: timeout exceeded\r\n')
                        self.socket.close()
                        return
                    else:
                        self.socket.settimeout(TIMEOUT - elapsed)
                index = stringbuffer.find('\r\n')
                commandstring = stringbuffer[:index]
                # print commandstring
                command = commandstring.split()
                stringbuffer = stringbuffer[index+2:]
                c, c2 = checkCommand(command)
                if state != AFTER_DATA and c == ILLEGAL:
                    # illegal command
                    self.socket.send('502 5.5.2 Error: command not recognized\r\n')
                elif state == IDLE:
                    if c!=HELO:
                        self.socket.send('503 Error: need HELO command\r\n')
                    else:
                        if len(command)<2:
                            self.socket.send('501 Syntax: HELO yourhostname\r\n')
                        elif len(command)>2:
                            self.socket.send('501 Syntax: Space found in hostname after HELO\r\n')
                        else:
                            clientname = command[1]
                            state = AFTER_HELO
                            # state transitioned to AFTER_HELO
                            self.socket.send("250 zr54\r\n")
                            self.socket.settimeout(TIMEOUT)
                            starttime = datetime.now()
                elif state == AFTER_HELO:
                    if c == HELO:
                        self.socket.send('503 Error: duplicate HELO\r\n')
                    elif c != MAIL_FROM:
                        self.socket.send('503 Error: need MAIL FROM command\r\n')
                    else:
                        if len(command) < 3 + c2:
                            self.socket.send('501 Syntax: MAIL FROM <email address>\r\n')
                        elif len(command) > 3 + c2:
                            i = commandstring.find(command[2+c2], commandstring.find(':')+2)
                            badEmail = commandstring[i:]
                            self.socket.send('504 5.5.2 <%s>: Sender address rejected\r\n' % badEmail)
                        else:
                            sender = command[2+c2]
                            state = AFTER_FROM
                            # state transitioned to AFTER_FROM
                            self.socket.send('250 2.1.0 OK\r\n')
                            self.socket.settimeout(TIMEOUT)
                            starttime = datetime.now()
                elif state == AFTER_FROM:
                    if c == MAIL_FROM:
                        self.socket.send('503 5.5.1 Error: nested MAIL command\r\n')
                    elif c != RCPT_TO:
                        self.socket.send('503 Error: need RCPT TO command\r\n')
                    else:
                        if len(command) < 3 + c2:
                            self.socket.send('501 Syntax: RCPT TO <email address>\r\n')
                        elif len(command) > 3 + c2:
                            i = commandstring.find(command[2+c2], commandstring.find(':')+2)
                            badEmail = commandstring[i:]
                            self.socket.send('504 5.5.2 <%s>: Recipient address invalid\r\n' % badEmail)
                        else:
                            recipients.append(command[2+c2])
                            state = AFTER_TO
                            # state transitions to AFTER_TO
                            self.socket.send('250 2.1.5 OK\r\n')
                            self.socket.settimeout(TIMEOUT)
                            starttime = datetime.now()
                elif state == AFTER_TO:
                    if c == RCPT_TO:
                        if len(command) < 3 + c2:
                            self.socket.send('501 Syntax: RCPT TO <email address>\r\n')
                        elif len(command) > 3 + c2:
                            i = commandstring.find(command[2+c2], commandstring.find(':')+2)
                            badEmail = commandstring[i:]
                            self.socket.send('504 5.5.2 <%s>: Recipient address invalid\r\n' % badEmail)
                        else:
                            recipients.append(command[2+c2])
                            # state is still AFTER_TO
                            self.socket.send('250 2.1.5 OK\r\n')
                            self.socket.settimeout(TIMEOUT)
                            starttime = datetime.now()
                    elif c != DATA:
                        self.socket.send('503 Error: need DATA or RCPT TO command\r\n')
                    else:
                        if len(command)>1:
                            self.socket.send('501 Syntax: No argument allowed for DATA\r\n')
                        else:
                            state = AFTER_DATA
                            # state transitions to AFTER_DATA
                            self.socket.send("354 End data with <CR><LF>.<CR><LF>\r\n")
                            self.socket.settimeout(TIMEOUT)
                            starttime = datetime.now()
                elif state == AFTER_DATA:
                    if commandstring == '.':
                        with ConnectionHandler.lock:
                            while ConnectionHandler.locked:
                                ConnectionHandler.cond.wait()
                            ConnectionHandler.locked = True
                            ConnectionHandler.count += 1
                            tmpcount = ConnectionHandler.count
                            f.write('Received: from ' + clientname + ' by zr54 (CS4410MP3)\n'
                                + 'Number: %d\n' % ConnectionHandler.count
                                + 'From: ' + sender + '\n'
                                + 'To: ' + ', '.join(recipients) + '\n\n'
                                + '\n'.join(data) + '\n\n')
                            f.flush()
                            if tmpcount % backupGroup == 0:
                                # backup mailbox in groups of 32
                                copyfile('mailbox', 'mailbox.%d-%d' %
                                 (tmpcount - backupGroup + 1, tmpcount))
                                f.close()
                                f = open('mailbox', 'w')
                            ConnectionHandler.locked = False
                            ConnectionHandler.cond.notify()
                        self.socket.send("250 OK: delivered message %d\r\n" % tmpcount)
                        state = AFTER_HELO
                        self.socket.settimeout(TIMEOUT)
                        starttime = datetime.now()
                        recipients = []
                        data = []
                    else:
                        data.append(commandstring)

            except socket.timeout:
                self.socket.send('421 4.4.2 zr54 Error: timeout exceeded\r\n')
                self.socket.close()
                return
            except socket.error:
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

# DO NOT CHANGE BELOW THIS LINE

opts, args = getopt.getopt(sys.argv[1:], 'h:p:', ['host=', 'port='])

for k, v in opts:
    if k in ('-h', '--host'):
        host = v
    if k in ('-p', '--port'):
        port = int(v)

print("Server coming up on %s:%i" % (host, port))
serverloop()
