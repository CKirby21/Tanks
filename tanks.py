import pygame, sys
from pygame.locals import *
import math

class Player():

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.startPosition = position
        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.downPressed = False
        self.shootPressed = False
        self.wasShot = False
        self.bullets = []
        self.width = PIXEL 
        self.height = PIXEL

        image = pygame.image.load("tank.png").convert_alpha()
        self.image = pygame.transform.scale(image, (self.width, self.height))

    def SetPressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shootPressed = True
        if event.type == pygame.KEYDOWN:
            if event.key == K_d: self.rightPressed = True
            if event.key == K_a: self.leftPressed = True
            if event.key == K_w: self.upPressed = True
            if event.key == K_s: self.downPressed = True
        elif event.type == pygame.KEYUP:
            if event.key == K_d: self.rightPressed = False
            if event.key == K_a: self.leftPressed = False
            if event.key == K_w: self.upPressed = False
            if event.key == K_s: self.downPressed = False

    def Move(self):
        X, Y = self.position[0], self.position[1]
        if self.rightPressed:
            X += self.velocity
        if self.leftPressed:
            X -= self.velocity
        if self.upPressed:
            Y -= self.velocity
        if self.downPressed:
            Y += self.velocity
        self.position = X, Y

    def Shoot(self):
        if self.shootPressed and len(self.bullets) < 4:
            bullet = Bullet(self.position, VELOCITY * 2)
            self.bullets.append(bullet)
        self.shootPressed = False

    def CollideWithBoundary(self):
        halfWidth = self.width // 2
        halfHeight = self.height // 2
        if self.position[1] + halfHeight > WINDOW_HEIGHT:
            self.position = self.position[0], WINDOW_HEIGHT - halfHeight
        if self.position[1] < 0 + halfHeight:
            self.position = self.position[0], 0 + halfHeight
        if self.position[0] + halfWidth > WINDOW_WIDTH:
            self.position = WINDOW_WIDTH - halfWidth, self.position[1]
        if self.position[0] < 0 + halfWidth:
            self.position = 0 + halfWidth, self.position[1]

    def Render(self):
        mx, my = pygame.mouse.get_pos()
        direction = mx - self.position[0], my - self.position[1]
        rotImage = RotateImage(self.image, direction, 0)
        rotImageRect = rotImage.get_rect(center = self.position)
        WINDOW.blit(rotImage, rotImageRect.topleft)

    def RenderBullets(self):
        for b in self.bullets:
            b.Move()
            b.Reflect()
            b.Render()
        for b in self.bullets:
            if b.velocity == 0:
                self.bullets.remove(b)

class Bullet():

    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.width = PIXEL // 6
        self.height = PIXEL // 12
        self.reflectionsLeft = 1

        image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.ComputeDirection()
    
    def ComputeDirection(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        EuclidDistance = lambda x, y: math.sqrt((x**2) + (y**2))
        vectorX, vectorY = mouseX-self.position[0], mouseY-self.position[1]
        length = EuclidDistance(vectorX, vectorY)
        self.direction = vectorX / length, vectorY / length

    def Move(self):
        X = self.position[0] + (self.direction[0] * self.velocity)
        Y = self.position[1] + (self.direction[1] * self.velocity)
        self.position = X, Y

    def Render(self):
        rotatedImage = RotateImage(self.image, self.direction, 0)
        rotatedRect = rotatedImage.get_rect(center = self.position)
        WINDOW.blit(rotatedImage, rotatedRect.topleft)

    def Reflect(self):
        dx, dy = self.direction[0], self.direction[1]
        halfWidth = self.width // 2
        halfHeight = self.height // 2
        if self.position[1] + halfHeight > WINDOW_HEIGHT:
            self.position = self.position[0], WINDOW_HEIGHT - halfHeight
            dy = -dy
        if self.position[1] < 0 + halfHeight:
            self.position = self.position[0], 0 + halfHeight
            dy = -dy
        if self.position[0] + halfWidth > WINDOW_WIDTH:
            self.position = WINDOW_WIDTH - halfWidth, self.position[1]
            dx = -dx
        if self.position[0] < 0 + halfWidth:
            self.position = 0 + halfWidth, self.position[1]
            dx = -dx
        # If bullet has been reflected...
        if dx == -self.direction[0] or dy == -self.direction[1]:
            if self.reflectionsLeft <= 0:
                self.velocity = 0
            else:
                self.direction = dx, dy
                self.reflectionsLeft -= 1

def RotateImage(image, direction: tuple, correctionAngle: float):
    angle = math.degrees(math.atan2(-direction[1], direction[0])) - correctionAngle
    return pygame.transform.rotate(image, angle)

def Main(velocity, time, pixel, screen):    

    global WINDOW, WINDOW_WIDTH, WINDOW_HEIGHT, PIXEL, RED, BROWN, VELOCITY
    # Colors
    BACKGROUND = (255, 255, 255)
    RED = (255, 30, 70)
    BROWN = (175, 155, 96)

    # Globals
    WINDOW_WIDTH = int(screen)
    WINDOW_HEIGHT = int(screen)
    PIXEL = int(pixel)
    VELOCITY = int(velocity)

    # Pygame Setup
    pygame.init()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()

    player = Player(WINDOW.get_rect().center, VELOCITY)

    # Main game loop
    while True :
        CLOCK.tick(60)
    
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            
            player.SetPressed(event)
        
        # Process game elements
        WINDOW.fill(BACKGROUND)
        player.RenderBullets()
        player.Move()
        player.CollideWithBoundary()
        player.Shoot()
        player.Render()
        pygame.display.update()

if __name__ == '__main__':
    Main(4, 8, 100, 600)
    