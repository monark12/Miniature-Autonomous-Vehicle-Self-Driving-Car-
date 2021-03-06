import keras
from keras.models import model_from_json
from utils import servo
from utils import motor
import picamera
import cv2
import time


json_file = open('monark/model.json','r')
loaded_model_json = json_file.read()
json_file.close()

p_time = time.time()
cnn_model = model_from_json(loaded_model_json)
cnn_model.load_weights('monark/model.h5')

with picamera.PiCamera() as camera:
  camera.resolution = (640, 480)
  camera.framerate= 5
  #motor.forward(80)
  try:
    for filename in camera.capture_continuous('image.jpg', use_video_port = True):
      print('capture, %f'%(time.time()-p_time) )
      img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE).reshape(1, 480, 640, 1)
      p_time = time.time()
      pred=cnn_model.predict(img)
      if pred>1:
        pred=1
      elif pred<-1:
        pred=-1

      #servo.turn(pred)
      print pred, time.time()-p_time
      p_time=time.time()
         	   
  except KeyboardInterrupt:
    m.stop()
    sys.exit(0)
