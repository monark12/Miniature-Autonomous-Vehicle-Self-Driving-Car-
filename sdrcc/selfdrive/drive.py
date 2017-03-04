import keras
from keras.models import model_from_json
import scipy
from keras.optimizer import Adam
import servo
import motor
import picamera
import cv2


json_file = open('monark_pc/model_architecture.json','r')
loaded_model_json = json_file.read()
json_file.close()

cnn_model = model_from_json(loaded_model_json)
cnn_model.load_weights('monark_pc/model_weights.h5')


# adam = Adam(lr = 0.01, decay = 1e-4)
# cnn_model.compile(loss='mean_squared_error', optimizer = adam)

m = motor()
s =servo()
with picamera.PiCamera() as camera:
	camera.color_effects = (128,128)
    m.forward(80)
    try:
        for filename in camera.capture_continuous('image.jpg'):
        	img = cv2.imread('image.jpg').reshape(1, 480, 640, 1)
        	pred=cnn_model.predict(img)
        	if pred>1:
        		pred=1
        	elif pred<-1:
        		pred=-1

        	s.turn(pred*3)
         	   
    except KeyboardInterrupt:
    	m.stop()
    	sys.exit(0)