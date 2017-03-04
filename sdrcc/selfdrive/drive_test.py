import keras
from keras.models import model_from_json
# import scipy
# from keras.optimizer import Adam
# import servo
# import motor
# import picamera
import cv2
import os


img_dir = '../../training_data/final_image_data/'
images = os.listdir('../../training_data/final_image_data')

json_file = open('monark/model.json','r')
loaded_model_json = json_file.read()
json_file.close()

cnn_model = model_from_json(loaded_model_json)
cnn_model.load_weights('monark/model.h5')

for image in images: 
    img = cv2.imread(img_dir+image, cv2.IMREAD_GRAYSCALE).reshape(1, 480, 640, 1)
    pred=cnn_model.predict(img)
    if pred>1:
    	pred=1
    elif pred<-1:
    	pred=-1

    print(pred)
