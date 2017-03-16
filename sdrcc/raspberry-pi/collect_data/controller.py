import os
from time import gmtime, strftime, sleep, time
from util import motor, servo
from pynput import keyboard
import pandas as pd


class ControllerStack(object):
  def __init__(self):
    self.items = []

  def push(self, item):
    if item not in self.items:
      self.items.append(item)

  def pop(self):
    return self.items.pop()

  # def peek(self):
  #   return self.items[-1]

  # def isEmpty(self):
  #   return len(self.items) == 0


stack = ControllerStack()


class Controller(object):
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo(pin=4)
    self.angle = {'forward': 0, 'forward_left': -1, 'forward_right': 1}
    self.state = {'dir': None, 'action': None, 'timestamp': None}
    self.data_stack = pd.DataFrame([], columns=['dir', 'action', 'timestamp'])

  def on_press(self, key):
    try:
      if key.char == 'w':
        self.motor.forward(75)
        self.state['dir'] = self.angle['forward']
        self.state['action'] = 'pressed'
        self.state['timestamp'] = time()
        self.data_stack.loc[len(self.data_stack)] = [self.state['dir'], self.state['action'], self.state['timestamp']]
        state_stack.push(self.state['dir'])

      elif key.char == 'a':
        self.servo.left()
        self.state['dir'] = self.angle['forward_left']
        self.state['action'] = 'pressed'
        self.state['timestamp'] = time()
        self.data_stack.loc[len(self.data_stack)] = [self.state['dir'], self.state['action'], self.state['timestamp']]
        state_stack.push(self.state['dir'])

      elif key.char == 'd':
        self.servo.right()
        self.state['dir'] = self.angle['forward_left']
        self.state['action'] = 'pressed'
        self.state['timestamp'] = time()
        self.data_stack.loc[len(self.data_stack)] = [self.state['dir'], self.state['action'], self.state['timestamp']]
        state_stack.push(self.state['dir'])

      elif key.char == 'q':
        self.motor.stop()
        self.servo.center
        self.servo.stop()
        state_stack.save_and_exit()

    except AttributeError:
      print("You've pressed the wrong key!!!")

  def on_release(self, key):
    try:
      if key.char == 'w':
        self.motor.stop()
        self.state['dir'] = self.angle['forward']
        self.state['action'] = 'released'
        self.state['timestamp'] = time()
        state_stack.pop()
        self.data_stack.loc[len(self.data_stack)] = [self.state['dir'], self.state['action'], self.state['timestamp']]

      elif key.char == 'a':
        self.servo.center()
        self.state['dir'] = self.angle['forward_left']
        self.state['action'] = 'released'
        self.state['timestamp'] = time()
        state_stack.pop()
        self.data_stack.loc[len(self.data_stack)] = [self.state['dir'], self.state['action'], self.state['timestamp']]

      elif key.char == 'd':
        self.servo.center()
        self.state['dir'] = self.angle['forward_right']
        self.state['action'] = 'released'
        self.state['timestamp'] = time()
        state_stack.pop()
        self.data_stack.loc[len(self.data_stack)] = [self.state['dir'], self.state['action'], self.state['timestamp']]

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


def main():
  drive = Controller()

if __name__ == '__main__':
  main()
