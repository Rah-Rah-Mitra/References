import pygame
import sys
import SpriteSheet #Another python class

pygame.init()
win = pygame.display.set_mode((700,500))
pygame.display.set_caption("Wolf Animation") # https://opengameart.org/content/lpc-wolf-animation

class spritesheet():
    def __init__(self, image):
        self.sheet = image  #sprite-sheet image

    def get_image(self, frame_w, frame_h, width, height, scale, colour):
        image = pygame.Surface((width,height)).convert_alpha()          #Size of Sprite
        image.blit(self.sheet, (0,0) , ((frame_w*width), (frame_h*height) , width, height)) #Location of Sprite starting at                                           
        image = pygame.transform.scale(image, (width*scale,height*scale)) #Resize           ## width and height frames from (0,0)
        image.set_colorkey(colour) #Remove Sprite Background Colour
        self.rect = image.get_rect()
        return image

#Sprite is 32x64 before first half of sheet and 64x32 after
sprite_sheet_image = pygame.image.load('References\Games (2D)_Mechanics\Wolf_SpriteSheet.png').convert_alpha() 
sprite_sheet = SpriteSheet.spritesheet(sprite_sheet_image)


BLACK = (0,0,0)

animation_list = [] #(No.Frames(Hori),1/4|2/4|3-4/4,Frame(Vert),Width,Height)
animation_steps = [ (5,0,0,32,64),    # Action: 0  : Barking / Eating (Forward)
                    (4,0,1,32,64),    # Action: 1  : Jumping / Sleeping (Forward) (Single Iteration for sleep)
                    (4,0,2,32,64),    # Action: 2  : Walking (Forward)
                    (5,0,3,32,64),    # Action: 3  : Running (Forward)
                    (5,0,4,32,64),    # Action: 4  : Chomping (Forward)
                    (4,5,1,32,64),    # Action: 5  : Taking Damage (Forward)/(Upward)
                    (4,5,2,32,64),    # Action: 6  : Climbing (Upward)
                    (5,5,3,32,64),    # Action: 7  : Howling (Upward)
                    (5,5,4,32,64),    # Action: 8  : Attacking (Upward)
                    (4,5,0,64,32),    # Action: 9  : Sleeping (Right)
                    (4,5,2,64,32),    # Action: 10 : Barking / Eating (Right)
                    (5,5,3,64,32),    # Action: 11 : Walking (Right)
                    (5,5,4,64,32),    # Action: 12 : Running (Right)
                    (5,5,5,64,32),    # Action: 13 : Chomping (Right)
                    (4,5,6,64,32),    # Action: 14 : Sleeping (Left)
                    (4,5,8,64,32),    # Action: 15 : Barking / Eating (Left)
                    (5,5,9,64,32),    # Action: 16 : Walking (Left)
                    (5,5,10,64,32),   # Action: 17 : Running (Left)
                    (5,5,11,64,32)]   # Action: 18 : Chomping (Left)

last_update = pygame.time.get_ticks()
animation_cooldown = 100 #ms
frame = 0 #Which stage of the animation it is in the flim
action = 7 #Which flim it is under animation steps / use buttons to control

for animation in animation_steps:
    temp_img_list = []
    (a,b,c,d,e) = animation
    for _ in range(a):
        temp_img_list.append(sprite_sheet.get_image(b+_,c,d,e,2,BLACK))
    animation_list.append(temp_img_list)

while True:
    win.fill((50,50,50))
    #Update Animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    win.blit(animation_list[action][frame], (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            X = 1
            action += X
            if action <= -20:         
                X *= -1
                frame = 0
            if action >= 19: 
                X *= -1
                frame = 0

    pygame.display.flip()
    pygame.time.Clock().tick(60)