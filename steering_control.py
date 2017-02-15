import pygame
from pygame.locals import *
import copy
import time
import datetime

pygame.init()

screen = pygame.display.set_mode((100,100))

print(pygame.event.get())



steering_data = []



#[forward, stop, left, right, timestamp]
 
while(True):
	for event in pygame.event.get():
		if event.type == KEYDOWN:
	
			if event.key == K_UP:
				ts = time.time()
				#forward()
				st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
				#this will convert the raw timestamp output
				# to hour:minute:second format
				# it would be easier to examine the data
				# @gautam if you want to change it you can if you want to
				steering_data.append([1,0,0,0,st])
			
			elif event.key == K_DOWN:
				ts = time.time()
				#stop()
				st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
				steering_data.append([0,1,0,0,st])
				
			
			elif event.key == K_LEFT:
				ts = time.time()
				#left()
				st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
				steering_data.append([0,0,1,0,st])

			elif event.key == K_RIGHT:
				ts = time.time()
				#rightt()
				st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
				steering_data.append([0,0,0,1,st])
			
			else:
				steering_data.append()

		elif event.type == KEYUP:
			print('released')
