"""
TODO:
* create methods if needed
"""
import RPi.GPIO as io

class Motor(object):
	def __init__(self, in1_pin=22, in2_pin=27, delayed=0, mode="pwm", frequency=500, active=1):
		io.setmode(io.BCM)
		io.setup(self.in1_pin, io.OUT)
		io.setup(self.in2_pin, io.OUT)
		self.set("delayed", str(self.delayed))
		self.set("mode", self.mode)
		self.set("frequency", str(self.frequency))
		self.set("active", str(self.active))

	def set(property, value):
		try:
			f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
			f.write(value)
			f.close()
		except:
			print("Error writing to: " + property + " value: " + value)

	def forward():
		io.output(self.in1_pin, True) 
		io.output(self.in2_pin, False)

	def reverse():
		io.output(self.in1_pin, False)
		io.output(self.in2_pin, True)

	def stop():
		io.output(self.in1_pin, False)
		io.output(self.in2_pin, False)

	def throttle(direction, speed):
		"""
		car's throttle

		inputs
		------
		direction (string): forward, reverse or stop
		speed (int): 0,...,9
		"""
		if direction == "forward":
			self.clockwise()
		elif direction == "stop":
			self.stop()
		else:
			self.reverse()
		self.set("duty", str(int(speed)*11))
		

# def main():
# 	pass

# if __name__ == '__main__':
	# main()


# while True:
	# cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
	# direction = cmd[0]
	# if direction == "f":
	# 	clockwise()
	# else:
	# 	counter_clockwise()
	# speed = int(cmd[1]) * 11
	# set("duty", str(speed))
