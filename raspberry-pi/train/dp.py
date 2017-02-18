import os

import numpy as np

imgs_path = 'training_images/'
imgs_ts_path = 'img-ts-1.npz'
angs_file = 'steer-1.npz'

imgs_ls = os.listdir(imgs_path)
imgs_ts = np.load(imgs_ts_path)
assert len(imgs_ls) == len(imgs_ts)
angs = np.load(angs_file)['steering_angle']
angs_ts = np.load(angs_file)['steering_timestamps']
assert len(angs) == len(angs_ts)


