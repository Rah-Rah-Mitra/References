import pygame
from PIL import Image
from pygame.locals import *
import sys
import random

pygame.init()
win = pygame.display.set_mode((800,800))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



    pygame.display.flip()
    pygame.time.Clock().tick(60)