import socket
import time
import picamera

#Define the streaming method
def camera_stream(passed_socket):    
    while 1:
        #listen for a new connection
        passed_socket.listen(5)
        print 'Server listening for connection'    

        #Accept a new connection
        conn = passed_socket.accept()
        print 'Accepted Connection'
    
        #Initialize Camera
        camera = picamera.PiCamera()
        camera.resolution = (360,240)
        camera.framerate = 24        
        camera.vflip = True
        camera.hflip = True

        #Make a file out of the connection to write video to
        file = conn[0].makefile('wb')
    
        #Try to write to connection file
        try:
            while 1:
                camera.start_recording(file, format='h264')
                camera.wait_recording(1)
                camera.stop_recording()
                #print 'Wrote data to connection'
    
        finally:
            connection.close()
            camera.close()    

        sleep(0.1)

#Create a TCP socket on the Raspberry Pi
tcp_sock = socket.socket()
tcp_ip = ''
tcp_port = 8767
tcp_sock.bind((tcp_ip, tcp_port))

camera_stream(tcp_sock)
