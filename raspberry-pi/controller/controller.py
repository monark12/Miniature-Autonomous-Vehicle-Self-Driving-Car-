import sys
import time
from time import gmtime, strftime
from util import motor
from util import servo
import pygame
from pygame.locals import *

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
            self.steering_angle.append([1,0,0,0])

          elif event.key == K_DOWN:
            print("stop")
            self.motor.stop()
            self.steering_angle.append([0,1,0,0])

          elif event.key == K_LEFT:
            print("left")
            self.servo.left()
            self.steering_angle.append([0,0,1,0])

          elif event.key == K_RIGHT:
            print("right")
            self.servo.right()
            self.steering_angle.append([0,0,0,1])


        # key is down
        elif event.type == KEYUP:
          print("released")
          if event.key == K_UP:
            self.motor.stop()

          elif event.key == K_DOWN:
            pass

          elif event.key == K_LEFT:
            self.servo.center()

          elif event.key == K_RIGHT:
            self.servo.center()

        # key is pressed and down
        else:
          self.steering_angle.append(self.steering_angle[:-1])
      

def main():
  c = Controller()
  c.steer()

if __name__ == '__main__':
 main()

