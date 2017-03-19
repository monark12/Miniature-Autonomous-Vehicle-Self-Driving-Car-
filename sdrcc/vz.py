import numpy as np
import cv2
import pandas as pd
import scipy.misc
import time
# Visualize images
# With and without any predictions
def visualize_data(filename, width=72, height=48, depth=3, cnn_model=None):
  """
  When cnn_model is specified it'll show what the cnn_model predicts (red)
  as opposed to what inputs it actually received (green)
  """
  data = pd.read_csv(filename)   
  print(data[:2])
  print(list(data.columns.values))

  for i in data.index:
    cur_img = data.loc[i,'id']
    cur_throttle = (data.loc[i,'mean_last_11_frames'])*100
    cur_motor = 100   # 100 -> just for testing (can be changed)
    
    # [1:-1] is used to remove '[' and ']' from string 
    #cur_img_array = scipy.misc.imread('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/final_image_data/'+cur_img+'.0.jpg')    
    cur_img_array = scipy.misc.imread('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/final_image_data/'+cur_img+'.jpg')    
    y_input = cur_img_array.copy() # NN input

    # And then rescale it so we can more easily preview it
    cur_img_array = cv2.resize(cur_img_array, (480, 320), interpolation=cv2.INTER_CUBIC)

    # Extra debugging info (e.g. steering etc)
    cv2.putText(cur_img_array, "frame: %s" % str(i), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    cv2.line(cur_img_array, (240, 300), (int(240+cur_throttle), 200), (0, 255, 0), 3)

    # Motor values
    # RGB
    cv2.line(cur_img_array, (50, 160), (50, 160-(90-cur_motor)), 100, 3)

    # If we wanna visualize our cnn_model
    if cnn_model:
      y = cnn_model.predict([y_input])
      servo_out = cnn_to_raw(y[0])     
      cv2.line(cur_img_array, (240, 300), (240-(90-int(servo_out)), 200), (0, 0, 255), 3)

      # can determine the motor our with a simple exponential equation
      # x = abs(servo_out-90)
      # motor_out = (7.64*e^(-0.096*x)) - 1
      # motor_out = 90 - motor_out
      x_ = abs(servo_out - 90)
      motor_out = (7.64*np.e**(-0.096*x_)) - 1
      motor_out = int(80 - motor_out) # only wanna go forwards
      cv2.line(cur_img_array, (100, 160), (100, 160-(90-motor_out)), raw_motor_to_rgb(motor_out), 3)
      print(motor_out, cur_motor)

    # Show frame
    # Convert to BGR cause thats how OpenCV likes it
    cv2.imshow('frame', cv2.cvtColor(cur_img_array, cv2.COLOR_RGB2BGR))
    # time.sleep(0.1)
    if cv2.waitKey(0) & 0xFF == ord('q'):

      break
    # time.sleep(0.1)  

visualize_data('/home/monark/LEARNINGS/Projects/SDC/sdrcc/training_data/final.csv')


  
