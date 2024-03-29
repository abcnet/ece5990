import socket
import time
import picamera
import sys

#Define the streaming method
def camera_stream():    
    while 1:
        try:
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
            with  picamera.PiCamera() as camera:
                
                camera.resolution = (640,480)
                camera.framerate = 30
                camera.vflip = True
                camera.hflip = True

                #Make a file out of the connection to write video to
                file = conn[0].makefile('wb')
            
                #Try to write to connection file
                # try:
                while 1:
                    camera.start_recording(file, format='h264')
                    camera.wait_recording(15)
                    camera.stop_recording()
                    #print 'Wrote data to connection'
        
        except:
            tcp_sock.close()
            camera.close()
               
        time.sleep(0.1)

camera_stream()
#if __name__ == '__main__'
#   camera_stream()
