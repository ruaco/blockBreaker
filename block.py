import pygame
from util import rect_intersects


class Block:
    def __init__(self, position):
        self.image = pygame.image.load("images/block.png")
        self.alive = True
        self.x = position[0]
        self.y = position[1]
        rect = self.image.get_rect()
        self.width = rect.right - rect.left
        self.height = rect.bottom - rect.top

    def kill(self):
        self.alive = False

    def size(self):
        return [self.width, self.height]

    def position(self):
        return [self.x, self.y]

    def collide(self, o):
        return self.alive and (rect_intersects(self, o) or rect_intersects(o, self))
