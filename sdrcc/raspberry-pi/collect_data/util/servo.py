import time
import pigpio

class Servo(object):
  def __init__(self, pin):
    self.pin = pin
    self.pi = pigpio.pi() # Connect to local Pi.

  def center(self):
    self.pi.set_servo_pulsewidth(self.pin, 2150);
    time.sleep(.02) #### to be changed

  def left(self):
    self.pi.set_servo_pulsewidth(self.pin, 1950); #2050
    time.sleep(.02) #### to be changed

  def right(self):
    self.pi.set_servo_pulsewidth(self.pin, 2350);
    time.sleep(.02) #### to be changed

  def fl(self,fac):
    self.pi.set_servo_pulsewidth(self.pin, int(2150+(-fac)*(2150-1950))); #2050
    time.sleep(.02) #### to be changed
     
  def fr(self,fac):
    self.pi.set_servo_pulsewidth(self.pin,int(2150+fac*(2350-2150))); #2050
    time.sleep(.02) #### to be changed
     
