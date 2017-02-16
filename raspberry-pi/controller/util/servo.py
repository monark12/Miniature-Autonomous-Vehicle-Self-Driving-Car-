import time
import pigpio

class Servo(object, pin):
  def __init__(self, pin):
    self.pin = pin
    self.pi = pigpio.pi() # Connect to local Pi.

  def center(self):
    self.pi.set_servo_pulsewidth(servo, 2250);
    time.sleep(.5) #### to be changed

  def left(self):
    self.pi.set_servo_pulsewidth(servo, 2000);
    time.sleep(.5) #### to be changed

  def right(self):
    self.pi.set_servo_pulsewidth(servo, 2500);
    time.sleep(.5) #### to be changed

