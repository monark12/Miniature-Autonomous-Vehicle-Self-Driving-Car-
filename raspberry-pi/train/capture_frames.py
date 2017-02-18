import numpy as np
import time
import picamera

frames_ts = [] # frames time stamps

try:
  with picamera.picamera() as camera:
    camera.resolution = (320, 240)
    # start a preview and let the camera warm up for 2 seconds
    time.sleep(2)
    
    i=0
    while True:
      camera.capture('training_images/image%d.jpg'%(i))
      frames_ts.append(time.time())
      time.sleep(.2)
      i+=1

except KeyboardInterrupt:
  frames_ts = np.array(frames_ts)
  np.saves('img-ts-1.npz', frames_ts=frames_ts)