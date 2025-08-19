import pygame
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
class Ball(pygame.sprite.Sprite):
   
    def __init__(self, window_width, window_height):
        super().__init__()
        self.image = pygame.image.load("ball_image.png")
        self.rect = self.image.get_rect()
        self.rect.center = (window_width // 2, window_height // 2)
        self.score=0
        self.lives=3
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1
       # if self.rect.bottom >= WINDOW_HEIGHT:S
            #self.speed_y *= -1

