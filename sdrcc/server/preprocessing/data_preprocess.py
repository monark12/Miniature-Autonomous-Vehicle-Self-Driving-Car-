"""
Take all the image and steering angle data,
get 1-1 image-angle mapping for each folder
and save the mapping as foo.csv in each data folder
"""
import os
from matplotlib import pylab 
import imageio
import csv
import pickle
import numpy as np
import pandas as pd

class Pointer(object):
  angle_df_pointer = None

class Stack(object):
  def __init__(self):
    self.__items = []

  def push(self, __item):
    if __item not in self.__items:
      self.__items.append(__item)

  def pop(self):
    if not self.isEmpty():
      return self.__items.pop()

  def peek(self):
    return self.__items[-1]

  def isEmpty(self):
    return len(self.__items) == 0


def bucket(timestamp, angle_df):
  for i in range(len(angle_df)):
    if timestamp >= angle_df.loc[i]['start_timestamp'] and timestamp <= angle_df.loc[i]['end_timestamp']:
      print(i)
      Pointer.angle_df_pointer = i
      return angle_df.loc[i]['angle']
  print('nan')
  return np.nan #ideally nan shouldn't be returned
                #always release all keys before quitting 
                #controller.py (this may be fixed in the future)
  

train_folders = os.listdir('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data')
for folder in train_folders:
  Pointer.angle_df_pointer = 0
  if os.path.isdir('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'+folder) and len(os.listdir('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'+folder)):
    # steer-1.csv --> steering angle (direction), action and timestamp
    data_stack = pd.read_csv('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'+folder+'/steer-1.csv')

    # start-ts-1.pkl --> start time of video recording
    with open('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'+folder+'/start-ts-1.pkl', 'rb') as f:
      start_time = pickle.load(f)

    # load mp4 video
    filename = '/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'+folder+'/video1.mp4'
    vid = imageio.get_reader(filename,  'ffmpeg')

    # extract start and end time for each action
    angle_df = pd.DataFrame(columns=['angle', 'start_timestamp', 'end_timestamp'])
    stack = Stack()
    for i in range(len(data_stack)):
      angle,action,timestamp = data_stack.loc[i]['angle'],data_stack.loc[i]['action'],data_stack.loc[i]['timestamp']
      if action == 'pressed':
        stack.push([angle, timestamp])
      elif action == 'released':
        start_ts = stack.pop()[1]
        end_ts = timestamp
        angle_df.loc[len(angle_df)] = [angle, start_ts, end_ts]

    sync_df = pd.DataFrame(columns=['id', 'angle'], dtype = int)
    for num, image in enumerate(vid.iter_data()):
      timestamp = float(num) / 15.
      timestamp += start_time
      if timestamp >= angle_df.loc[0]['start_timestamp'] and timestamp <= angle_df.loc[len(angle_df)-1]['end_timestamp']:
        # print(num)
        sync_df.loc[len(sync_df)] = [num, bucket(timestamp, angle_df)]

    # remove records where angle is NaN
    sync_df = sync_df.dropna().reset_index(drop=True)
    #sync_df = sync_df[sync_df.angle==np.nan].reset_index(drop=True)        


    for i in range(len(sync_df)):
      pylab.imsave('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/final_image_data/#'+folder+'-'+str(int(sync_df.id.values[i]))+'.jpg', vid.get_data(int(sync_df.id.values[i])))
      sync_df.loc[i,'id'] = '#'+folder+'-'+str(int(sync_df.id.values[i]))
      print(i, sync_df.values[i])
      pylab.close()
    print(folder)
    
    sync_df = sync_df.dropna().reset_index(drop=True)

    sync_df.to_csv("/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/"+folder+"/sync.csv", index=False)

