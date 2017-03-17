import os
from time import gmtime, strftime, sleep, time
from util import motor, servo
from pynput import keyboard
import pandas as pd
import sys

SPEED = 80

class Stack(object):
  def __init__(self):
    self.__items = []

  def push(self, __item):
    if __item not in self.__items:
      self.__items.append(item)

  def pop(self):
    if not self.isEmpty():
      return self.__items.pop()

  def peek(self):
    return self.__items[-1]

  def isEmpty(self):
    return len(self.__items)==0

state_stack = Stack()


class Controller(object):
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo(pin=4)
    self.angle = {'forward': 0, 'forward_left': -1, 'forward_right': 1}
    self.data_stack = pd.DataFrame( columns=['angle', 'action', 'timestamp'])

  def on_press(self, key):
    try:
      if key.char == 'w':
        self.motor.forward(SPEED)
        self.data_stack.loc[len(self.data_stack)] = [self.angle['forward'], 'pressed', time()]
        state_stack.push(self.angle['forward'])

      elif key.char == 'a':
        self.servo.left()
        self.data_stack.loc[len(self.data_stack)] = [self.angle['forward_left'], 'pressed', time()]
        state_stack.push(self.angle['forward_left'])

      elif key.char == 'd':
        self.servo.right()
        self.data_stack.loc[len(self.data_stack)] = [self.angle['forward_right'], 'pressed', time()]
        state_stack.push(self.angle['forward_right'])

      elif key.char == 'q':
        self.motor.stop()
        self.servo.center
        self.servo.stop()
        self.save_and_exit()

    except Exception as e:
      print(e)
      #print("You've pressed the wrong key!!!")

  def on_release(self, key):
    try:
      if key.char == 'w':
        self.motor.stop()
        self.data_stack.loc[len(self.data_stack)] = [state_stack.pop(), 'released', time()]

      elif key.char == 'a':
        self.servo.center()
        self.data_stack.loc[len(self.data_stack)] = [state_stack.pop(), 'released', time()]

      elif key.char == 'd':
        self.servo.center()
        self.data_stack.loc[len(self.data_stack)] = [state_stack.pop(), 'released', time()]

    except AttributeError:
      print("You've pressed the wrong key!!!")

  def steer(self):
    with keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release) as listener:
      listener.join()

  def save_and_exit(self):
    print("saving")
    self.data_stack.to_csv('data/steer-1.csv', index=False)
    print("exiting")
    sys.exit()


def main():
  drive = Controller()
  drive.steer()

if __name__ == '__main__':
  main()
