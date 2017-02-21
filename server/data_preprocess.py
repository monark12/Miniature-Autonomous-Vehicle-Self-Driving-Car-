from matplotlib import pylab
import imageio
import csv
import pickle
import numpy as np

# steer-1.npz --> steering angles and timestamps
steering_data = np.load('steer-1.npz')
steering_angle = steering_data['steering_angle']
steering_timestamp = steering_data['steering_timestamp']

# start-ts-1.pkl--> start time of video recording
with open('start-ts-1.pkl', 'rb') as f:
  start_time = pickle.load(f)

# load mp4 video
filename = 'video1.mp4'
vid = imageio.get_reader(filename,  'ffmpeg')


def find_closest_timestamp(search_list, search_element):
  """Get closest matching timestamp to <search_element> from <search_list>"""
  return min(search_list, key=lambda t:abs(t-search_element))


def multidim_intersect(arr1, arr2):
  """Get intersection between multidimensional arrays"""
  arr1 = np.array(arr1)
  arr2 = np.array(arr2)
  arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
  arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
  intersected = np.intersect1d(arr1_view, arr2_view)
  return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])


frame_to_angle_ts = []
angle_to_frame_ts = []
temp_time_stamp = []

try:
  # get time stamps of every frame in video and
  # corresponding steering angle to each frame based on time stamps
  # get 1-1 mapping of each frame to corresponding steering_angle
  for num, image in enumerate(vid.iter_data()):
    timestamp = float(num) / 8.
    temp_time_stamp.append(start_time+timestamp)
    frame_to_angle_ts.append([num, find_closest_timestamp(steering_timestamp, start_time+timestamp)])

  # get 1-1 mapping of each steering_angle to corresponding frame
  for i, steering_ts in enumerate(steering_timestamp):
    angle_to_frame_ts.append([temp_time_stamp.index(find_closest_timestamp(temp_time_stamp, steering_ts)), steering_ts])

  # remove records where car was not moving
  clean_data = multidim_intersect(frame_to_angle_ts, angle_to_frame_ts)

  # replace timestamp in clean_data by steering angle
	#### optimize this without using temp 
  temp = []
  steering_timestamp = list(steering_timestamp)
  for i, steer_ts in enumerate(clean_data[:,1]):
    temp.append(steering_angle[steering_timestamp.index(steer_ts)])
  # temp=[0]*len(temp)
  clean_data[:,1] = np.array(temp)
  clean_data = clean_data.astype(np.int64)
  del temp

  print(temp)
  # print(clean_data)
  # for i in range(len(clean_data)):
  #   clean_data[i,1] = int(temp[i])


  # save cleaned data
  for index in clean_data[:,0]:
    pylab.imsave('imgs/frame%d.jpg'%int(index), vid.get_data(int(index)))
    pylab.close()


except RuntimeError:
  print('something went wrong')


np.savetxt("foo.csv", clean_data, delimiter=',')