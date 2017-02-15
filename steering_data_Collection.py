import pygame
from pygame.locals import *
import copy

pygame.init()

screen = pygame.display.set_mode((100,100))

print(pygame.event.get())



while(True):
 key_event = pygame.key.get_pressed()
 if key_event[pygame.K_UP]:
  print('u')
 


while(True):
 flag = False
 for event in pygame.event.get():
  if event.type == KEYDOWN:
   start = event
   if event.key == K_UP:
    print('forward')
   elif event.key == K_DOWN:
    print('down')
   else:
    break

  elif event.type == KEYUP:
   print('released')
