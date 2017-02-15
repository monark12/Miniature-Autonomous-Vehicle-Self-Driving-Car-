"""
TODO:
* study about PWM from coursera video
* comment time.sleep in "turn" method if turning is not smooth
* decide digital or analog turn and create coressponding methods
"""
import RPi.GPIO as GPIO
import time


class Servo(object):
  def __init__(self, channel=4, frequency=100, duty_cycle=5):
    self.channel = channel
    self.frequency = frequency
    self.duty_cycle = duty_cycle
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.channel, GPIO.OUT)
    self.pwm = GPIO.PWM(self.channel, self.frequency)
    self.pwm.start(self.duty_cycle)

  def turn(self, angle):
    self.pwm.ChangeDutyCycle(float(angle) / 10.0 + 2.5)
    time.sleep(1) 


def main():
  s = Servo()
  s.turn(50)
#  s.turn(0) 
#  s.turn(12) 
#  s.turn(25) 
#  s.turn(37) 
#  s.turn(50) 
  pass

if __name__ == '__main__':
  main()
