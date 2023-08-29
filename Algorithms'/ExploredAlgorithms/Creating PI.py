
import pygame

pygame.init()
clock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WHITE = (255, 255, 255)
pygame.font.init()
textfont = pygame.font.SysFont("monospace", 30)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PI")
screen.fill((0,0,0))
s1 = pygame.Surface((60,60))
s1.fill((255,0,0))
s1.set_alpha(255)

class Object():
    def __init__(self, mass, velocity,surface,pos):
        self.mass = mass
        self.velocity = velocity
        self.surface = surface
        self.pos = pos

collisions = 0
mass1 = 1000000
s = pygame.Surface((300, 300))
s.fill((0, 0, 255))
m1 = Object(mass1,-500,s,390)
m2 = Object(1,0,s1,300)
wall = pygame.Rect(35,500,5,300)

pygame.draw.line(screen,WHITE,(40,500),(40,0),5) #zid vert
pygame.draw.line(screen,WHITE,(800,450),(0,450),2)
time_step = 1000
fps = 1000

while True:
    clock.tick(fps)
    dt1, dt2 = clock.tick(fps) / 1000 , clock.tick(time_step) / 1000
    dt = dt1 * dt2
    r1 = pygame.Rect(m1.pos,450,60,60)
    r2 = pygame.Rect(m2.pos,450,60,60)
    for i in range(time_step):
        m1.pos += m1.velocity * dt
        m2.pos += m2.velocity * dt
        if m1.pos <= m2.pos + 60:
            collisions += 1
            old_vel, old_vel2= m1.velocity, m2.velocity
            m1.velocity = (m1.mass - m2.mass) / (m1.mass + m2.mass) * old_vel + (2 * m2.mass) / (
                    m1.mass + m2.mass) * m2.velocity
            m2.velocity = (2 * m1.mass) / (m1.mass + m2.mass) * old_vel + (m2.mass - m1.mass) / (
                    m1.mass + m2.mass) * old_vel2
        elif m2.pos <= 40 and m2.velocity < 0 :
            m2.velocity *= -1
            collisions+=1
    pygame.Surface.fill(screen, (0, 0, 0))
    pygame.draw.line(screen, WHITE, (40, 500), (40, 0), 5)  # vertical wall
    pygame.draw.line(screen, WHITE, (800, 450), (0, 450), 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.blit(m1.surface, (m1.pos,150))
    screen.blit(m2.surface, (m2.pos,390))
    textTBD = textfont.render("Colisions:"+ str(collisions), True, (255,0 ,0 ))
    screen.blit(textTBD, (500,60))
    pygame.display.flip()
