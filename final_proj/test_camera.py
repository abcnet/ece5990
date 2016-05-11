import socket
import time
import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_HOST = socket.gethostname() 
UDP_PORT = 8001
print socket.gethostbyname(UDP_HOST)
server_socket.bind((UDP_HOST, UDP_PORT))

initial_socket = socket.socket()
TCP_HOST = ''
TCP_PORT = 8000
initial_socket.bind((TCP_HOST, TCP_PORT))
initial_socket.listen(5)
print 'Socket now listening'

#Accept a single connection and make a file-like object out of it
accepted_conn = initial_socket.accept()
connection = accepted_conn[0].makefile('wb')
client_addr = accepted_conn[1][0]

#Create user UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = client_addr
UDP_PORT = 5000



try:
    camera.start_recording(connection, format='h264')
    camera.wait_recording(10)
    camera.stop_recording()
finally:
    connection.close()
    initial_socket.close()
    #server_socket.close()
    #time.sleep(30);
    camera.close()
