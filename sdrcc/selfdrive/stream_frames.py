import io
import numpy as np
import socket
import struct
import time
import picamera
#from threading import Thread
from multiprocessing import Process

# arrays to be saved
frame_id = []
angles = []
ts = []


# connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
print('bef con')
client_socket.connect(('192.168.0.6', 8000))
print('aft con')

import controller 
c = controller.Controller()
#t = Thread(target=c.steer)
#t.start()

P = Process(target=c.steer)
P.start()
# make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    # start a preview and let the camera warm up for 2 seconds
    camera.framerate = 5

    # note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()

    # start steering in another thread
    
    i = 0
    for foo in camera.capture_continuous('stream.jpg', use_video_port=True):
      # write the length of the capture to the stream and flush to
      # ensure it actually gets sent
      connection.write(struct.pack('<l', stream.tell()))
      connection.flush()
      # rewind the stream and send the image data over the wire
      stream.seek(0)
      connection.write(stream.read())

      frame_id.append(i)
      angles.append(c.steering_angle[:-1])
      ts.append(time.time())
      
      # if we've been capturing for more than 30 seconds, quit
      if time.time() - start > 120: # run for 2 minutes
        break
      # reset the stream for the next capture
      stream.seek(0)
      stream.truncate()
    i += 1
  # write a length of zero to the stream to signal we're done
  connection.write(struct.pack('<l', 0))
finally:
  frame_id = np.array(frame_id)
  angles = np.array(angles)
  ts = np.array(ts)
  np.savez("steering-1.npz", frame_id=frame_id, angles=angles, ts=ts)
  connection.close()
  client_socket.close()
