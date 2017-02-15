#!/usr/bin/env python

import time

import pigpio

servos = [4,7,8,9,10]

moves = [[1500, 5],[1400,3],[1300,2],[1200,5],[1100,10]]

pi = pigpio.pi() # Connect to local Pi.

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
