from matplotlib import pylab
import imageio

filename = 'video1.mp4'
vid = imageio.get_reader(filename,  'ffmpeg')
try:
  for num, image in enumerate(vid.iter_data()):
    fig = pylab.figure()
    pylab.imshow(image)
    timestamp = float(num)/ 8.0
    print(timestamp)
    fig.suptitle('image #{}, timestamp={}'.format(num, timestamp), fontsize=20)
    pylab.show()

except RuntimeError:
  print('something went wrong')

