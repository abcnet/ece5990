import socket
import time
import picamera

client_IP = 10.148.4.134

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
camer.hflip = True
camera.vflip = True


#Accept TCP connection from client, then get its IP address
#NOT DOING THIS RIGHT NOW
#create while loop that writes .h264 files and sends them via UDP


#create termination functionality

#after proof of concept, make it into a method


# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_HOST = ''
TCP_PORT = 8004
client_socket.connect((TCP_HOST, TCP_PORT))
client_socket.listen(5)

# Make a file-like object out of the connection
connection = client_socket
try:
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        camera.wait_recording(60)
        camera.stop_recording()
finally:
    connection.close()
    client_socket.close()
    camera.close()
