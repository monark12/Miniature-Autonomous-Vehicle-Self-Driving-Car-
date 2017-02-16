"""
*** Turn wheels by hand to give pwm a start at low duty cycle
TODO:
* create methods if needed
"""
import RPi.GPIO as io
import pygame
from pygame.locals import *
import time

pygame.init()########
screen = pygame.display.set_mode((100,100))

class Motor(object):
  def __init__(self, in1_pin=22, in2_pin=27, delayed=0, mode="pwm", duty_cycle=70, frequency=500, active=1):
    self.in1_pin = in1_pin
    self.in2_pin = in2_pin
    self.delayed = delayed
    self.mode = mode
    self.frequency = frequency
    self.duty_cycle = duty_cycle
    self.active = active
    io.setmode(io.BCM)
    io.setup(self.in1_pin, io.OUT)
    io.setup(self.in2_pin, io.OUT)
    self.pwm = io.PWM(self.in1_pin, self.frequency)
    
  def forward(self, speed):
    self.pwm.start(speed)
    io.output(self.in2_pin, False)

  def stop(self):
    self.pwm.stop()
    io.output(self.in1_pin, False)
    io.output(self.in2_pin, False)

print(pygame.event.get())


m = Motor()
while(True):
 for event in pygame.event.get():
  if event.type == KEYDOWN:
   if event.key == K_UP:
    m.forward(70)
   elif event.key == K_DOWN:
    m.stop()
   else:
    break

  elif event.type == KEYUP:
    m.pwm.stop()
##m.forward()
