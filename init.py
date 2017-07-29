import pygame
import sys
import time
from util import log, rect_intersects


size = width, height = 400, 300


class Ball:
    def __init__(self):
        self.image = pygame.image.load("images/ball.png")
        rect = self.image.get_rect()
        self.width = rect.left - rect.right
        self.height = rect.top - rect.bottom
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
            if self.x < 0 or self.x > 400:
                self.speed_x *= -1
            if self.y < 0 or self.y > 300:
                self.speed_y *= -1
            self.x += self.speed_x
            self.y += self.speed_y

    def rebound(self):
        self.speed_y *= -1


class Block:
    def __init__(self, position):
        self.image = pygame.image.load("images/block.png")
        self.alive = True
        self.x, self.y = position
        rect = self.image.get_rect()
        self.width = rect.left - rect.right
        self.height = rect.top - rect.bottom

    def kill(self):
        self.alive = False

    def size(self):
        return [self.width, self.height]

    def position(self):
        return [self.x, self.y]

    def collide(self, o):
        return self.alive and rect_intersects(self, o) and rect_intersects(o, self)


class Paddle:
    def __init__(self):
        self.image = pygame.image.load("images/paddle.png")
        self.x = 100
        self.y = 250
        rect = self.image.get_rect()
        self.width = rect.right - rect.left
        self.height = rect.top - rect.bottom
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
        return self.x < ball.x < self.x + self.width and ball.y - ball.height >= self.y


class Game:
    actions = {}
    keydowns = {}
    _fps = 100
    ball = None
    paddle = None

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(size)
        self.screen = screen

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                for i in self.actions:
                    if key[i] == 1:
                        self.keydowns[i] = True
            if event.type == pygame.KEYUP:
                key = pygame.key.get_pressed()
                for i in self.actions:
                    if key[i] == 0:
                        self.keydowns[i] = False

    def register_action(self, key, func):
        self.actions[key] = func

    def draw_image(self, i):
        self.screen.blit(i.image, i.position())

    def update(self):
        ball = self.ball
        paddle = self.paddle
        ball.move()
        if paddle.collide(ball):
            ball.rebound()

    def draw(self, **kwargs):
        for i in kwargs.keys():
            if i == 'ball':
                self.ball = kwargs.get(i)
            if i == 'paddle':
                self.paddle = kwargs.get(i)
        ball = self.ball
        paddle = self.paddle
        if ball is not None and paddle is not None:
            self.draw_image(ball)
            self.draw_image(paddle)

    def clear(self):
        self.screen.fill([0, 0, 0])

    def run(self):
        while True:
            self.event_listener()
            actions = self.actions.keys()
            for k in actions:
                if self.keydowns.get(k):
                    self.actions.get(k)()
            self.update()
            self.clear()
            self.draw()
            pygame.display.flip()
            time.sleep(1/self._fps)


def __main():

    g = Game()

    ball = Ball()
    paddle = Paddle()

    g.register_action(pygame.K_LEFT, paddle.move_left)
    g.register_action(pygame.K_RIGHT, paddle.move_right)
    g.register_action(pygame.K_SPACE, ball.fire)
    g.register_action(pygame.K_ESCAPE, sys.exit)
    g.draw(ball=ball, paddle=paddle)

    g.run()

if __name__ == '__main__':
    __main()
