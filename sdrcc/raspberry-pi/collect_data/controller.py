import sys
import os
import time
from time import gmtime, strftime
from util import motor
from util import servo
#import pygame
#from pygame.locals import *
import numpy as np
from pynput import keyboard

#pygame.init()
#screen = pygame.display.set_mode((50,50))

class Controller(object):
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo(4)
    self.steering_angle = []
    self.steering_timestamp = []
    self.dir = {'forward': 0, 'forward_left': 1, 'forward_right': 2}

  def on_press(self, key):
    try:
      if key.char == 'w':
        self.steering_timestamp.append(time.time())
        print("forward")
        self.motor.forward(85)
        self.steering_angle.append(self.dir['forward'])
  
      elif key.char == 'a':
        self.steering_timestamp.append(time.time())
        print("forward-left")
        self.servo.left()
        self.steering_angle.append(self.dir['forward_left'])
  
      elif key.char == 'd':
        self.steering_timestamp.append(time.time())
        print("forward-right")
        self.servo.right()
        self.steering_angle.append(self.dir['forward_right'])

      elif key.char == 'q':
        self.save_and_exit()
        # Stop listener
        return False

    except AttributeError:
      print("You've pressed the wrong key!!!")

  def on_release(self, key):
    try:
      if key.char == 'w':
        self.motor.stop()
  
      elif key.char == 'a':
        self.steering_timestamp.append(time.time())
        self.servo.center()
        self.steering_angle.append(self.dir['forward'])
  
      elif key.char == 'd':
        self.steering_timestamp.append(time.time())
        self.servo.center()
        self.steering_angle.append(self.dir['forward'])
  
    except AttributeError:
      print("You've pressed the wrong key!!!")

  def steer(self):
    with keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release) as listener:
      listener.join()

  def save_and_exit(self):
    print("saving")
    self.steering_angle = np.array(self.steering_angle)
    self.steering_timestamp = np.array(self.steering_timestamp)
    np.savez("data/steer-1.npz", steering_angle=self.steering_angle, steering_timestamp=self.steering_timestamp)
    print("exiting")
    #os.system('scp steer-1.npz monark@192.168.0.6:/home/sdrcc/training_data/')
    #os.system('scp steer-1.npz gautamsharma@192.168.0.2:/home/projects/sdrcc/training_data/')


class ControllerStack(object):
  def __init__(self):
    self.items = []

  def push(self, item):
    self.items.append(item)

  def pop(self):
     return self.items.pop()

  def peek(self):
     return self.items[-1]

  def isEmpty(self):
     return len(self.items) == 0

def main():
  c = Controller()
  c.steer()

if __name__ == '__main__':
  main()

