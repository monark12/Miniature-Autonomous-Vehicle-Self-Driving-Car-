import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm = GPIO.PWM(17, 100)
pwm.start(5)

def update(angle):
	duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)

def main():
	while(False):
		for i in range(50):
			update(i)
			time.sleep(0.05)
		for i in range(50):
			update(50-i)
			time.sleep(0.05)

	while(True):
		update(0)
		time.sleep(0.2)
		update(12)
		time.sleep(0.2)
		update(25)
		time.sleep(0.2)
		update(37)
		time.sleep(0.2)
		update(50)
		time.sleep(0)
		time.sleep(0.2)
		update(12)
		time.sleep(0.2)
		update(25)
		time.sleep(0.2)
		update(37)
		time.sleep(0.2)
		update(50)
		time.sleep(0.2)

update(25)
try:
    pass
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
