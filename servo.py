"""
TODO:
* study about PWM from coursera video
* comment time.sleep in "turn" method if turning is not smooth
* decide digital or analog turn and create coressponding methods
"""
import RPi.GPIO as GPIO
import time


class Servo(object):
  def __init__(self, channel=17, frequency=100, duty_cycle=5):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.channel, GPIO.OUT)
    self.pwm = GPIO.PWM(self.channel, self.frequency)
    self.pwm.start(self.duty_cycle)

  def turn(angle):
    self.pwm.ChangeDutyCycle(float(angle) / 10.0 + 2.5)
    time.sleep(0.02) 


# def main():
#   pass

# if __name__ == '__main__':
  # main()
