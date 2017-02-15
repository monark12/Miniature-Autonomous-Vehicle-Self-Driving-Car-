"""
TODO:
* create methods if needed
"""
import RPi.GPIO as io
import pygame
from pygame.locals import *
import time

pygame.init()
screen = pygame.display.set_mode((100,100))

class Motor(object):
  def __init__(self, in1_pin=22, in2_pin=27, delayed=0, mode="pwm", frequency=500, active=1):
    self.in1_pin = in1_pin
    self.in2_pin = in2_pin
    self.delayed = delayed
    self.mode = mode
    self.frequency = frequency
    self.active = active
    self.duty_cycle =50#############
    io.setmode(io.BCM)
    io.setup(self.in1_pin, io.OUT)
    io.setup(self.in2_pin, io.OUT)
    self.pwm = io.PWM(self.in1_pin, self.frequency)
    
#    self.set("delayed", str(self.delayed))
##    self.set("mode", self.mode)
##    self.set("frequency", str(self.frequency))
##    self.set("active", str(self.active))
##    self.set('duty', str(50))

     

  def set(self, property, value):
    try:
      f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
      f.write(value)
      f.close()
    except:
      print("Error writing to: " + property + " value: " + value)

  def forward(self, speed):
    
    #self.pwm.ChangeDutyCycle(float(speed)*11)
    self.pwm.start(self.duty_cycle)
    io.output(self.in2_pin, False)


  def reverse(self):
    io.output(self.in1_pin, False)
    io.output(self.in2_pin, True)
    time.sleep(2)
    io.output(self.in2_pin, False)

  def stop(self):
    io.output(self.in1_pin, False)
    io.output(self.in2_pin, False)

  def throttle(self, direction, speed):
    """
    car's throttle

    inputs
    ------
    direction (string): forward, reverse or stop
    speed (int): 0,...,9
    """
    if direction == "forward":
      self.forward(speed)
    elif direction == "stop":
      self.stop()
    else:
      self.reverse()
    

# def main():
#   pass

# if __name__ == '__main__':
  # main()

print(pygame.event.get())


m = Motor()
while(True):
 for event in pygame.event.get():
  if event.type == KEYDOWN:
   if event.key == K_UP:
    m.forward(2)
   elif event.key == K_DOWN:
    m.reverse()
   else:
    break

  elif event.type == KEYUP:
    m.stop()
    m.pwm.stop()
##m.forward()
