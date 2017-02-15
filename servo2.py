import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
pwm = GPIO.PWM(4, 100)
pwm.start(5)

def update(angle):
	duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)

def main():
	while(True):
		for i in range(50):
			update(i)
			time.sleep(0.05)
		for i in range(50):
			update(50-i)
			time.sleep(0.05)

main()
