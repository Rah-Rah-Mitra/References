import pygame

class spritesheet():
    def __init__(self, image):
        self.sheet = image  #sprite-sheet image

    def get_image(self, frame_w, frame_h, width, height, scale, colour):
        image = pygame.Surface((width,height)).convert_alpha()          #Size of Sprite
        image.blit(self.sheet, (0,0) , ((frame_w*width), (frame_h*height) , width, height)) #Location of Sprite starting at                                           
        image = pygame.transform.scale(image, (width*scale,height*scale)) #Resize           ## width and height frames from (0,0)
        image.set_colorkey(colour) #Remove Sprite Background Colour
        return image
