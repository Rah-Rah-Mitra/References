import pygame
from pygame.locals import *
import sys

TBLR = [True,True,True,True]
def Draw_Hollow():
    x,y = 0,0
    L,B = 50,5
    if TBLR[0]:
        pygame.draw.line(win,(0,0,0),(x,y),(x+L,y),B) # Top
    if TBLR[1]:
        pygame.draw.line(win,(0,0,0),(x,y+L),(x+L,y+L),B) # Bottom
    if TBLR[2]:
        pygame.draw.line(win,(0,0,0),(x,y),(x,y+L),B) # Left
    if TBLR[3]:
        pygame.draw.line(win,(0,0,0),(x+L,y),(x+L,y+L),B) # Right

pygame.init()
win = pygame.display.set_mode((800,800))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    win.fill((255,255,255))
    Draw_Hollow()
    #TBLR[0] = False
    TBLR[1] = False
    #TBLR[2] = False
    TBLR[3] = False


    pygame.display.flip()
    pygame.time.Clock().tick(60)