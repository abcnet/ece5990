import socket
import time
import picamera


camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

UDP_HOST = '0.0.0.0'
UDP_PORT = 8000
server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(0)
print 'Socket now listening'

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
try:
    camera.start_recording(connection, format='h264')
    camera.wait_recording(10)
    camera.stop_recording()
finally:
    connection.close()
    server_socket.close()
# time.sleep(30);
    camera.close()
