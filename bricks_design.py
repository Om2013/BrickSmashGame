import pygame
import random 

class Bricks(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        bricks=["bricks1.jpg","bricks2.jpg","bricks3.jpg"]
        self.image = pygame.image.load(bricks[random.randint(0,2)])
        new_size=(80,20)
        self.image=pygame.transform.scale(self.image,new_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
