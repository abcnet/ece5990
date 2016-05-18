import socket
import time
import picamera
import sys
import errno
from socket import error as socket_error

#Define the streaming method
def camera_stream(control):    
    if (control == 1):
    while control:
        #Create a TCP socket on the Raspberry Pi
        tcp_sock = socket.socket()
        tcp_ip = ''
        tcp_port = 8767
        tcp_sock.bind((tcp_ip, tcp_port))

        #listen for a new connection
        tcp_sock.listen(5)
        print 'Server listening for connection'    

        #Accept a new connection
        conn = tcp_sock.accept()
        print 'Accepted Connection'
    
        #Initialize Camera
        camera = picamera.PiCamera()
        camera.resolution = (1920,1080)
        camera.framerate = 24        
        camera.vflip = True
        camera.hflip = True

        #Make a file out of the connection to write video to
        file = conn[0].makefile('wb')
    
        #Try to write to connection file
        try:
            while 1:
                camera.start_recording(file, format='h264')
                camera.wait_recording(15)
                camera.stop_recording()
                #print 'Wrote data to connection'
    
        except:
            #conn.close()
            tcp_sock.close()
            camera.close()
               
        time.sleep(0.1)


camera_stream()

#if __name__ == '__main__'
#   camera_stream()
