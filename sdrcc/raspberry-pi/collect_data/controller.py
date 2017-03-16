import os
import time
from time import gmtime, strftime
from util import motor
from util import servo
from threading import Thread
from pynput import keyboard
import numpy as np


class ControllerStack(object):
  def __init__(self):
    self.items = []
    self.steering_angle = []
    self.steering_timestamp = []
    self.LISTENER_ACTIVE = False    

  def set_active(self):
    self.LISTENER_ACTIVE = True

  def set_deactive(self):
    self.LISTENER_ACTIVE = False  
  
  def push(self, item):
    if item not in self.items:
      self.items.append(item)

  def pop(self):
    return self.items.pop()

  def peek(self):
    return self.items[-1]

  def isEmpty(self):
    return len(self.items) == 0

  def run(self):
    print('running')
    while True:
      time.sleep(0.1)
      if self.LISTENER_ACTIVE and not self.isEmpty():
        print(self.peek())
        self.steering_timestamp.append(time.time())
        self.steering_angle.append(self.peek())

  def save_and_exit(self):
    print("saving")
    self.steering_angle = np.array(self.steering_angle)
    self.steering_timestamp = np.array(self.steering_timestamp)
    np.savez("data/steer-1.npz", steering_angle=self.steering_angle, steering_timestamp=self.steering_timestamp)
    print("exiting")
    os._exit(1)

stack = ControllerStack()

      
class Controller(object):
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo(pin=4)
    self.dir = {'forward': 0, 'forward_left': -1, 'forward_right': 1}

  def on_press(self, key):
    try:
      if key.char == 'w':
        stack.set_active()
        self.motor.forward(75)
        stack.push(self.dir['forward'])
 
      elif key.char == 'a':
        stack.set_active()
        self.servo.left()
        stack.push(self.dir['forward_left'])

      elif key.char == 'd':
        stack.set_active()        
        self.servo.right()
        stack.push(self.dir['forward_right'])

      elif key.char == 'q':
        self.motor.stop()
        self.servo.center
        self.servo.stop()
        stack.save_and_exit() 

    except AttributeError:
      print("You've pressed the wrong key!!!")

  def on_release(self, key):
    try:
      if key.char == 'w':
        stack.set_deactive()
        self.motor.stop()
  
      elif key.char == 'a':
        stack.pop()
        self.servo.center()
  
      elif key.char == 'd':
        stack.pop()
        self.servo.center()

    except AttributeError:
      print("You've pressed the wrong key!!!")
  
  def steer(self):
    with keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release) as listener:
      listener.join()

def main():
  drive = Controller()
  Thread(target=drive.steer).start()
  Thread(target=stack.run).start()

if __name__ == '__main__':
  main()

