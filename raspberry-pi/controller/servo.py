#!/usr/bin/env python

import time

import pigpio

servo = 4

pi = pigpio.pi() # Connect to local Pi.

pi.set_servo_pulsewidth(servo, 2500);
time.sleep(10)
pi.set_servo_pulsewidth(servo, 0);

while True:
 pass

moves = [[1500, 5],[1400,3],[1300,2],[1200,5],[1100,10]]


for m in moves:

   for s in servos:

      pw = m[0] + (s*50) # give each servo different pulsewidth for demo

      pi.set_servo_pulsewidth(s, pw)

      print("Servo {} {} micro pulses".format(s, pw))

   time.sleep(m[1])

   # switch all servos off

   for s in servos:
      pi.set_servo_pulsewidth(s, 0);

pi.stop()
