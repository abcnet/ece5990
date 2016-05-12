import socket
import time
import picamera




def camera_stream():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 24

    initial_socket = socket.socket()
    TCP_HOST = ''
    TCP_PORT = 8
    initial_socket.bind((TCP_HOST, TCP_PORT))
    initial_socket.listen(5)
    print 'Socket now listening'

    #Accept a single connection and make a file-like object out of it
    accepted_conn = initial_socket.accept()
    connection = accepted_conn[0].makefile('wb')
    client_addr = accepted_conn[1][0]
    
    try:
        camera.start_recording(connection, format='h264')
        camera.wait_recording(60)
        camera.stop_recording()
    finally:
        connection.close()
        initial_socket.close()
        #server_socket.close()
        #time.sleep(30);
        camera.close()
