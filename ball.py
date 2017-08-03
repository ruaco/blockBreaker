import pygame


class Ball:
    def __init__(self):
        self.image = pygame.image.load("images/ball.png")
        rect = self.image.get_rect()
        self.width = rect.right - rect.left
        self.height = rect.bottom - rect.top
        self.x = 100
        self.y = 200
        self.speed_x = 3
        self.speed_y = 3
        self.fired = False

    def size(self):
        return [self.width, self.height]

    def position(self):
        return [self.x, self.y]

    def fire(self):
        self.fired = True

    def move(self):
        if self.fired:
            if self.x < 0 or self.x > 400 - self.width:
                self.speed_x *= -1
            if self.y < 0 or self.y > 300 - self.height:
                self.speed_y *= -1
            self.x += self.speed_x
            self.y += self.speed_y

    def rebound(self):
        self.speed_y *= -1
