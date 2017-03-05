import time
import sys
import struct
import socket
import picamera
import numpy as np
import io
#import controller 
from util import servo
from util import motor

#######sending
client_socket = socket.socket()
print('bef con')
client_socket.connect(('192.168.0.6', 8000))
print('aft con')
######

#######recieving
server_socket = socket.socket()
server_socket.bind(('192.168.0.5', 8000))
server_socket.listen(0)
#######

#c = controller.Controller()

connection = client_socket.makefile('wb')
recieve_connection = server_socket.accept()[0].makefile('rb')

try:
  with picamera.PiCamera() as camera:
    camera.resolution = (640,480)
    camera.framerate = 5

    stream = io.BytesIO()
    
    for image in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
      connection.write(struct.pack('<l',stream.tell()))
      connection.flush()
      print(stream, type(stream))
      stream.seek(0)
      connection.write(stream.read())
      
      stream.seek(0)
      stream.truncate()
      connection.write(struct.pack('<l',0))


      # receive
      #steering_angle = float(server_socket.recv(24))
      steering_angle = struct.unpack('d', server_socket.recv(24))[0]
      servo.turn(steering_angle)
      #motor.foward(80)
  


except KeyboardInterrupt:
  sys.exit(-1)

finally:
  connection.close()
  client_socket.close()
