import numpy as np
import cv2
import pandas as pd
import scipy.misc
import time
import copy
import os

hyperparemeters = []
DIR = '/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/'
final = pd.DataFrame(columns=['id','angle'])

# Visualize images
# With and without any predictions
def visualize_data(filename, width=72, height=48, depth=3, cnn_model=None):
  """
  When cnn_model is specified it'll show what the cnn_model predicts (red)
  as opposed to what inputs it actually received (green)
  """
  global hyperparemeters, final
  cv2.namedWindow('image',cv2.WINDOW_NORMAL)
  cv2.resizeWindow('image', 1366,768)
  
  data = pd.read_csv(filename)
  data_columns = [column for column in data.columns.values[4:-1]]

  for i in data.index:
    cur_img = data.loc[i,'id']
    throttle_list = [(data.loc[i,column])*100 for column in data_columns]
    
    cur_motor = 100   # 100 -> just for testing (can be changed)
    
    # [1:-1] is used to remove '[' and ']' from string 
    #cur_img_array = scipy.misc.imread('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/final_image_data/'+cur_img+'.0.jpg')    
    cur_img_array = scipy.misc.imread(DIR+'final_image_data/'+cur_img+'.jpg')    
    y_input = cur_img_array.copy() # NN input

    # And then rescale it so we can more easily preview it
    cur_img_array = cv2.resize(cur_img_array, (480, 320), interpolation=cv2.INTER_CUBIC)
    
    #make copies of the input image
    image_copy_array = [copy.deepcopy(cur_img_array) for i in throttle_list]
    cv2.putText(image_copy_array[0], "frame: %s" % str(i), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 1, 255) 

    #insert line showing the current steering angle corresponding to the current image in all copies
    images_to_display = [cv2.line(image_copy_array[i], (240, 300), (int(240+throttle_list[i]), 200), (0, 255, 0), 3)
                          for i in range(len(throttle_list))]
    
    # Motor values
    # RGB
    # image_with_line = cv2.line(cur_img_array, (50, 160), (50, 160-(90-cur_motor)), 100, 3)

    image_visualization_grid1 = np.hstack(images_to_display[:3])
    image_visualization_grid2 = np.hstack(images_to_display[3:6])
    image_visualization_grid3 = np.hstack(images_to_display[6:])
    final_grid = np.vstack((image_visualization_grid1, image_visualization_grid2, image_visualization_grid3))

       
    # Show frame
    # Convert to BGR cause thats how OpenCV likes it
    cv2.imshow('image', cv2.cvtColor(final_grid, cv2.COLOR_RGB2BGR))
    if cv2.waitKey(0) & 0xFF == ord('q'):
      key = cv2.waitKey(0) & 0xFF
      hyperparemeters.append([folder, data_columns[int(chr(key))-1]])
      final = final.append(pd.DataFrame(data[['id', data_columns[int(chr(key))-1]]].values, columns=['id','angle']), ignore_index=True)
      
      break

for folder in os.listdir(DIR):
  if os.path.isdir(DIR+folder) and ('sync.csv' in os.listdir(DIR+folder)):
    visualize_data(DIR+folder+'/sync.csv')


final.to_csv(DIR+'final.csv', index=False)
  
