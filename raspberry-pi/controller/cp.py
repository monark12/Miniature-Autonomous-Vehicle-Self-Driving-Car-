import sys
import time
from time import gmtime, strftime
from util import motor
from util import servo
import pygame
from pygame.locals import *
import numpy as np

pygame.init()
screen = pygame.display.set_mode((100,100))

class Controller(object):
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo(4)
    self.steering_angle = []
    self.steering_timestamp = []

  def steer(self):
    while(True):
      for event in pygame.event.get():

        # key is pressed
        if event.type == KEYDOWN:

          if event.key == K_UP:
            print("forward")
            self.motor.forward(70)
            self.steering_angle.append([1,0])
            self.steering_timestamp.append(time.time())

          elif event.key == K_LEFT:
            print("left")
            self.servo.left()
            self.steering_angle.append([0,1])
            self.steering_timestamp.append(time.time())

          elif event.key == K_DOWN:
            self.save_and_exit()

        # key is down
        elif event.type == KEYUP:
          print("released")
          if event.key == K_UP:
            self.motor.stop()

          elif event.key == K_LEFT:
            self.servo.center()

        # key is pressed and down
        else:
          self.steering_angle.append(self.steering_angle[:-1])
          self.steering_timestamp.append(time.time())
      
  def save_and_exit(self):
    print("saving")
    np.savez("steer-1.npz", steering_angle=self.steering_angle, steering_timestamp=self.steering_timestamp)
    print("exiting")

def main():
  c = Controller()
  c.steer()

if __name__ == '__main__':
 main()

