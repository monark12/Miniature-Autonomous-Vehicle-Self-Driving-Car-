import time
import pickle

with open('start-ts-1.pkl', 'wb') as f:
	pickle.dump(time.time(), f)

