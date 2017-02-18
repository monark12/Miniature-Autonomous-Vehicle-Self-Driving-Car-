import time
import picamera

frames_ts = [] # frames time stamps

try:
  with picamera.PiCamera() as camera:
    camera.resolution = (320,240)
    camera.color_effects = (128,128)
    camera.framerate = 50
    time.sleep(2)
    for filename in camera.capture_continuous('training_images/img{counter:03d}.jpg'):
      print(i)

except KeyboardInterrupt:
  frames_ts = np.array(frames_ts)
  np.savez('img-ts-1.npz',frames_ts=frames_ts)
