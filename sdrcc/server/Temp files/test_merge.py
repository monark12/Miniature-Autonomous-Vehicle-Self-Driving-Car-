import cv2
import numpy as np
import pandas as pd

#cv2.imshow('image',img)

df = pd.read_csv('foo.csv')

imgs=df.F.values.tolist()
sas = df.A.values.tolist()
print(sas)

for i in range(len(imgs)): 
 img=cv2.imread('imgs/frame%d.jpg'%int(imgs[i]))
 cv2.imshow('image',img)
 if sas[i] == 0.:
  print('forward')
 if sas[i] == 1.:
  print('left')
 if sas[i] == 2.:
  print('right')
 cv2.waitKey(0)
cv2.destroyAllWindows()
  


