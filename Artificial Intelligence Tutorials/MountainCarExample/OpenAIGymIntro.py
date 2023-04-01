
import gym 
import pygame

env = gym.make("MountainCar-v0",render_mode="human") 
observation = env.reset() 

for _ in range(10000): 
  env.render()
  action = env.action_space.sample()
  result = env.step(action)
  
  if len(result) == 4:
      observation, reward, done, info = result
      print(observation, reward, done, info)
  else:
      print("Invalid result from step() method:", result)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
