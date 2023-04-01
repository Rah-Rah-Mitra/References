import pygame
import sys
import tensorflow as tf
import numpy as np
import random

pygame.init()
win_width = 400
win_height = 400
win = pygame.display.set_mode((400,400))

class objective(object):
    def __init__(self):
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect()
        self.colour = (0,255,0)
        self.rect.x = random.randrange(0,win_width,50) # Position of Rect X (Random)
        self.rect.y = random.randrange(0,win_height,50) # Position of Rect Y (Random)

class Moving_Object(object):
    def __init__(self):
        self.x , self.y = 8 , 8 # Speed relative to X  # Speed relative to Y
        self.width_height = (20,20)
        self.image =pygame.Surface(self.width_height)
        color = []
        for _ in range(10):
            color.append(((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255))))
        self.colour = color[random.randint(0,len(color)-1)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,win_width,50) # Position of Rect X (Random)
        self.rect.y = random.randrange(0,win_height,50) # Position of Rect Y (Random)
        
    def Draw(self):
        win.fill((255, 255, 255))
        pygame.draw.rect(win,self.colour,self.rect)
        pygame.draw.rect(win,Objective.colour,Objective.rect)
        pygame.display.update()

    def Border_Closed(self,action): 
        p = 10
        
        if action == 0:
            self.rect.x += self.x
        elif action == 1:
            self.rect.y += self.y
        elif action == 2:
            self.rect.x -= self.x
        elif action == 3:
            self.rect.y -= self.y

        if self.rect.right > win_width or self.rect.left < 0:
            self.x *= -1
        if self.rect.bottom > win_height or self.rect.top < 0:
            self.y *= -1       

        self.precision = p  # If depth of 1/(2**p) of cube nails into boundary Eject
        if ((2**p)*(self.rect.right) - self.rect.right + self.rect.centerx)/(2**p) > win_width:
            self.rect.x -= self.rect.width/(2**p)
        if ((2**p)*(self.rect.left) - self.rect.left + self.rect.centerx)/(2**p) < 0:
            self.rect.x += self.rect.width/(2**p)
        if ((2**p)*(self.rect.bottom) - self.rect.bottom + self.rect.centery)/(2**p) > win_height:
            self.rect.y -= self.rect.height/(2**p)
        if ((2**p)*(self.rect.top) - self.rect.top + self.rect.centery)/(2**p) < 0:
            self.rect.y += self.rect.height/(2**p)

        dist = ((self.rect.centerx - Objective.rect.centerx) ** 2 + (self.rect.centery - Objective.rect.centery) ** 2) ** 0.5
        reward = 1 / (1 + dist)
        done = self.rect.colliderect(Objective.rect)
        return np.array([self.rect.centerx / Objective.rect.centerx , self.rect.centery / Objective.rect.centery]), reward, done

    def Border_Open(self,action):
        if action == 0:
            self.rect.x += self.x
        elif action == 1:
            self.rect.y += self.y
        elif action == 2:
            self.rect.x -= self.x
        elif action == 3:
            self.rect.y -= self.y

        if self.rect.x > win_width :                                # Right to left Win
            self.rect.x = -abs(self.rect.right-self.rect.left)        
        if self.rect.x + abs(self.rect.right-self.rect.left) < 0 :  # Left to right Win
            self.rect.x = win_width
        if self.rect.y > win_height :                                # Bottom to top Win
            self.rect.y = -abs(self.rect.bottom-self.rect.top)
        if self.rect.y + abs(self.rect.bottom-self.rect.top) < 0 :  # Top to Bottom Win
            self.rect.y = win_height

        dist = ((self.rect.bottom - win_width) ** 2 + (self.rect.right - win_height) ** 2) ** 0.5
        reward = 1 / (1 + dist)
        done = self.rect.bottom >= win_width and self.rect.right >= win_height
        return np.array([self.rect.bottom/win_width,self.rect.right/win_height]), reward, done

# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, input_shape=(2,), activation='relu'),
    tf.keras.layers.Dense(4, activation='linear')
])
# Compile the model
model.compile(optimizer='adam', loss='mse')

Dot= Moving_Object()
Objective = objective()
Score = 0

# Train the agent
for i in range(1000):
    state = Dot.Border_Closed(0)[0]
    while True:
        Dot.Draw()
        action = np.argmax(model.predict(np.array([state])))
        next_state, reward, done = Dot.Border_Closed(action)
        # Create a one-hot encoded vector for the action
        target = model.predict(np.array([state]))
        target[0][action] = reward + 0.9 * np.max(model.predict(np.array([next_state])))
        # Fit the model
        model.fit(np.array([state]), target, epochs=1)
        state = next_state
        if done:
            Objective.rect.x = random.randrange(0,win_width,10) # Position of Rect X (Random)
            Objective.rect.y = random.randrange(0,win_height,10) # Position of Rect Y (Random)
            Score += 1
            # if Score == 10:
            break
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.flip()
        pygame.time.Clock().tick(200)