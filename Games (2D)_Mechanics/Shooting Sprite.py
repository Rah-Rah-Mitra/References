"""Smooth Movement in pygame"""
"""Smooth Shooting in pygame"""

#Imports
import pygame, sys
import random
import math

#Constants
WIDTH, HEIGHT = 400, 400
TITLE = "Smooth Movement"

#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.color = (0,255,255)
        self.width_height = (30,30)
        self.image =pygame.Surface(self.width_height)
        self.image.fill((0,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y # Position of Rect Y (Random)
        self.x = 0
        self.y = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.shoot = False
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        # BULLET COOLDOWN
        Cooldown = 200
        # PLAYER SPEED
        self.x = 2
        self.y = 2

        if self.left_pressed and not self.right_pressed:
            self.x *= -1
            self.rect.x += self.x
        if self.right_pressed and not self.left_pressed:
            self.x *= 1
            self.rect.x += self.x
        if self.up_pressed and not self.down_pressed:
            self.y *= -1
            self.rect.y += self.y
        if self.down_pressed and not self.up_pressed:
            self.y *= 1
            self.rect.y += self.y

        Time_Now = pygame.time.get_ticks()                              # The concept is that pygame.Rect will render the player
        if self.shoot and Time_Now - self.last_shot > Cooldown:         # So we set a timer to render the player each time it shoots
            bullet = Bullets(self.rect.centerx , self.rect.centery)     # So once a bullet is fired, player is rendered and the time
            bullet.image.fill((0,255,0))                                # Is saved as last_shot, so a cooldown function checks if 
            bullet_group.add(bullet)                                    # Time Now - Last shot > Cooldown, has finished cooldown
            self.last_shot = Time_Now
       
        self.rect = pygame.Rect(int(self.rect.x), int(self.rect.y), player.width_height[0], player.width_height[1])

class Bullets(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,10))
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		MouseX , MouseY = pygame.mouse.get_pos()
		self.bulletspeedx = 5
		self.bulletspeedy = 5
		self.X_Dis_Frm_M_Pos = player.rect.centerx - MouseX 
		self.Y_Dis_Frm_M_Pos =  player.rect.centery - MouseY

		self.Angle_M_Pos = abs(math.atan2(abs(self.Y_Dis_Frm_M_Pos),abs(self.X_Dis_Frm_M_Pos)))
		
		if self.X_Dis_Frm_M_Pos > 0 and self.Y_Dis_Frm_M_Pos > 0: #0
			self.bulletspeedy *= -1
			self.bulletspeedx *= -1
			self.rect.y += math.sin(self.Angle_M_Pos) * self.bulletspeedy
			self.rect.x += math.cos(self.Angle_M_Pos) * self.bulletspeedx
		if self.X_Dis_Frm_M_Pos < 0 and self.Y_Dis_Frm_M_Pos > 0: #1
			self.bulletspeedy *= -1
			self.bulletspeedx *= 1
			self.rect.y += math.sin(self.Angle_M_Pos) * self.bulletspeedy
			self.rect.x += math.cos(self.Angle_M_Pos) * self.bulletspeedx
		if self.X_Dis_Frm_M_Pos < 0 and self.Y_Dis_Frm_M_Pos < 0: #2
			self.bulletspeedy *= 1
			self.bulletspeedx *= 1
			self.rect.y += math.sin(self.Angle_M_Pos) * self.bulletspeedy
			self.rect.x += math.cos(self.Angle_M_Pos) * self.bulletspeedx
		if self.X_Dis_Frm_M_Pos > 0 and self.Y_Dis_Frm_M_Pos < 0: #3
			self.bulletspeedy *= 1
			self.bulletspeedx *= -1
			self.rect.y += math.sin(self.Angle_M_Pos) * self.bulletspeedy
			self.rect.x += math.cos(self.Angle_M_Pos) * self.bulletspeedx

        # IF BULLET EXCEEDS CERTAIN THERESHOLD KILL IT
		if self.rect.bottom < 0:
			self.kill()
		if self.rect.top > HEIGHT:
			self.kill()
		if self.rect.right < 0:
			self.kill()
		if self.rect.left > WIDTH:
			self.kill()

#Player Initialization
player = Player(WIDTH/2, HEIGHT/2)
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()

#Main Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False
        if event.type == pygame.MOUSEBUTTONUP:
            player.shoot = False

    #Draw
    win.fill((12, 24, 36))  

    player_group.draw(win)
    bullet_group.draw(win)

    #update
    player.update()
    bullet_group.update()

    pygame.display.flip()

    clock.tick(120)