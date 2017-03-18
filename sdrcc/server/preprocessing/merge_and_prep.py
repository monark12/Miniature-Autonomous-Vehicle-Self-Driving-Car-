"""
Take sync.csv in each data folder and concat into final.csv
Add mean columns
"""
import collections
import numpy as np
import pandas as pd
import os

DIR = '/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'
data_folders = os.listdir(DIR)
RANGE = (3,15)

#first file
# final = pd.read_csv(str(DIR)+'0/sync.csv', header=None)
final = pd.read_csv(str(DIR)+'1/sync.csv')

# # now the rest:
# for num, folder in enumerate(data_folders):
#   try:
#     if 'sync.csv' in os.listdir(str(DIR)+folder):
#       # temp = pd.read_csv(str(DIR)+folder+'/sync.csv', header=None)
#       temp = pd.read_csv(str(DIR)+folder+'/sync.csv')
#       final = pd.concat([final,temp], ignore_index=True)
#   except Exception:
#     pass

# final = final.drop_duplicates(subset='id') # drop duplicates
# final.to_csv(DIR+'final.csv', index=False)

# add regressive labels
# final = pd.read_csv(DIR+'final.csv')
n_mean_labels = []

for i in range(RANGE[0],RANGE[1]):
  x = collections.deque(i*[0], i)
  mean_labels = []
  for angle in final.angle.values:
    x.appendleft(angle)
    mean_labels.append(np.mean(x))
  n_mean_labels.append(mean_labels)

# add regressive labels to final.csv and save
for i in range(RANGE[0],RANGE[1]):
  final['mean_last_%d_frames'%i] = pd.Series(n_mean_labels[i-RANGE[0]], index=final.index)

final.to_csv(DIR+'final.csv', index=False)

