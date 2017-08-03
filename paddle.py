import pygame
from util import rect_intersects


class Paddle:
    def __init__(self):
        self.image = pygame.image.load("images/paddle.png")
        self.x = 100
        self.y = 250
        rect = self.image.get_rect()
        self.width = rect.right - rect.left
        self.height = rect.bottom - rect.top
        self.speed = 5

    def position(self):
        return [self.x, self.y]

    def move(self, x):
        if x < 0:
            x = 0
        if x > 400 - self.width:
            x = 400 - self.width
        self.x = x

    def move_left(self):
        self.move(self.x - self.speed)

    def move_right(self):
        self.move(self.x + self.speed)

    def collide(self, ball):
        return rect_intersects(self, ball) or rect_intersects(ball, self)
