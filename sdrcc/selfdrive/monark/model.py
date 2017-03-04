# import dataset_loader
import os
import sys
from keras.models import Sequential
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D, LSTM
from keras.optimizers import SGD, Adam
from keras.regularizers import l2
import random
import cv2
import pandas as pd
import numpy as np

train_batch_pointer = 0
test_batch_pointer = 0

image_data_dir = '../../../training_data/final_image_data/'
dataset = pd.read_csv('../../../training_data/final.csv')

X = dataset.id.values
y = dataset.mean_last_5_frames.values

c = list(zip(X, y))
random.shuffle(c)
X, y = zip(*c)

# X_train, X_val, y_train, y_val = train_val_split(X,y, val_size = 0.2)
X,y = np.array(X), np.array(y)
train_set_size = int(0.8 * len(X))
X_train = X[:train_set_size]
X_val = X[train_set_size:]
y_train = y[:train_set_size]
y_val = y[train_set_size:]

train_batch_pointer = 0
val_batch_pointer = 0


def load_train_batch(batch_size=32):
	global train_batch_pointer
	while True:

		train_batch_pointer = 0
		for i in range(int(len(X_train)/ batch_size)):
			batch_x = []
			batch_y = []
			for i in range(train_batch_pointer,train_batch_pointer+batch_size):
				batch_x.append(cv2.imread(image_data_dir+X_train[i]+'.jpg', cv2.IMREAD_GRAYSCALE)/225.)
				# batch_y.append(y_train[i])
			batch_x = np.array(batch_x).reshape(len(batch_x),480,640,1).astype('float32')
			batch_y = y_train[train_batch_pointer:train_batch_pointer+32]
			# print(batch_y[:10])

			yield (batch_x, batch_y)
			train_batch_pointer+=batch_size
			sys.stdout.write('\r'+str(train_batch_pointer))
			sys.stdout.flush()


def load_val_batch(batch_size=32):
	global val_batch_pointer
	while True:

		val_batch_pointer = 0
		for i in range(int(len(X_val)/ batch_size)):
			batch_x = []
			batch_y = []
			for i in range(val_batch_pointer,val_batch_pointer+batch_size):
				batch_x.append(cv2.imread(image_data_dir+X_val[i]+'.jpg', cv2.IMREAD_GRAYSCALE)/225.)
				# batch_y.append(y_val[i])
			batch_x = np.array(batch_x).reshape(len(batch_x),480,640,1).astype('float32')
			batch_y = y_val[val_batch_pointer:val_batch_pointer+32]
			# print(batch_y[:10])

			yield (batch_x, batch_y)
			val_batch_pointer+=batch_size
			sys.stdout.write('\r'+str(val_batch_pointer))
			sys.stdout.flush()



model = Sequential()

model.add(Convolution2D(8, 5, 5, border_mode='valid', input_shape=(480, 640,1), activation='relu'))
model.add(MaxPooling2D(pool_size=(5, 5)))

model.add(Convolution2D(12, 5, 5, activation='relu',border_mode='valid'))

model.add(MaxPooling2D(pool_size=(5, 5)))

model.add(Convolution2D(16, 5, 5, activation='relu'))



model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(1))

# print(model.summary())

adam = Adam(lr = 0.001. decay=1e-4)
model.compile(loss='mse', optimizer=adam)

if os.path.exists('model.h5'):
    model.load_weights('model.h5')

model.fit_generator(load_train_batch(), samples_per_epoch=len(X_train), nb_epoch=5, verbose=2, validation_data=load_val_batch(), nb_val_samples=len(X_val), class_weight=None)

model_json = model.to_json()
with open("model.json", "w") as json_file:
        json_file.write(model_json)
model.save('model.h5')
print("model saved")