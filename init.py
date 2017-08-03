import pygame
import sys
import time
from ball import Ball
from paddle import Paddle
from block import Block


class Game:
    _size = width, height = 400, 300
    _fps = 100

    actions = {}
    keydowns = {}
    score = 0

    ball = None
    paddle = None
    blocks = []

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(self._size)
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
            if event.type == pygame.QUIT:
                sys.exit()

    def register_action(self, key, func):
        self.actions[key] = func

    def draw_image(self, i):
        self.screen.blit(i.image, i.position())

    def draw_text(self, text, position):
        font = pygame.font.Font(None, 20)
        text_object = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_object, position)

    def update(self):
        ball = self.ball
        paddle = self.paddle
        ball.move()
        if paddle.collide(ball):
            ball.rebound()
        blocks = self.blocks
        for i in blocks:
            if i.collide(ball):
                i.kill()
                ball.rebound()
                self.score += 100

    def draw(self, **kwargs):
        for i in kwargs.keys():
            if i == 'ball':
                self.ball = kwargs.get(i)
            if i == 'paddle':
                self.paddle = kwargs.get(i)
            if i == 'blocks':
                self.blocks = kwargs.get(i)

        ball = self.ball
        if ball is not None:
            self.draw_image(ball)

        paddle = self.paddle
        if paddle is not None:
            self.draw_image(paddle)

        blocks = self.blocks
        if len(blocks) > 0:
            for i in blocks:
                if i.alive:
                    self.draw_image(i)

        self.draw_text('score: ' + str(self.score), [20, 20])

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
    blocks = []
    for i in range(7):
        blocks.append(Block([i*50+20, 100]))

    g.register_action(pygame.K_LEFT, paddle.move_left)
    g.register_action(pygame.K_RIGHT, paddle.move_right)
    g.register_action(pygame.K_SPACE, ball.fire)
    g.register_action(pygame.K_ESCAPE, sys.exit)
    g.draw(ball=ball, paddle=paddle, blocks=blocks)

    g.run()

if __name__ == '__main__':
    __main()
