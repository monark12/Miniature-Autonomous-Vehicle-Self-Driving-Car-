import sys
from time import gmtime, strftime
from util import motor
from util import servo

pygame.init()
screen = pygame.display.set_mode((100,100))

class Controller(object):
  def __init__(self):
    self.motor = motor.Motor()
    self.servo = servo.Servo()
    self.steering_angle = []
    self.steering_timestamp = []

  def steer(self):
    while(True):
      for event in pygame.event.get():

				# key is pressed
        if event.type == KEYDOWN:

          if event.key == K_UP:
            print("forward")
            self.servo.center()
            self.motor.forward(70)
            self.steering_angle.append([1,0,0,0])
            self.steering_timestamp.append(time.time())

          elif event.key == K_DOWN:
            print("stop")
            self.motor.stop()
            self.steering_angle.append([0,1,0,0])
            self.steering_timestamp.append(time.time())

          elif event.key == K_LEFT:
            print("left")
            self.servo.left()
            self.motor.forward(70)
            self.steering_angle.append([0,0,1,0])
            self.steering_timestamp.append(time.time())

          elif event.key == K_RIGHT:
            print("right")
            self.servo.right()
            self.motor.forward(70)
            self.steering_angle.append([0,0,0,1])
            self.steering_timestamp.append(time.time())

          elif event.key == K_q:
            self.save_and_exit()

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
          self.steering_angle.append(steering_angle[-1])
          self.steering_timestamp.append(time.time())

	def save_and_exit(self):
		print("saving...")
		self.steering_angle = np.array(self.steering_angle)
		self.steering_timestamp = np.array(self.steering_timestamp)
		np.savez("steering-%s"%(strftime("%Y-%m-%d %H:%M:%S", gmtime()))+".npz", steering_angle=self.steering_angle, steering_timestamp=self.steering_timestamp)
		print("quitting...")
		sys.exit(0)

