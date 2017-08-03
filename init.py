import pygame
import sys
import time
from ball import Ball
from paddle import Paddle
from block import Block


class Start:

    actions = {}
    keydowns = {}

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.register_action(pygame.K_r, self.enter)

    def draw_text(self, text, position):
        font = pygame.font.Font(None, 20)
        text_object = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_object, position)

    def draw(self):
        self.draw_text('start game', [160, 120])
        self.draw_text('reload game', [160, 140])
        self.draw_text('exit game', [160, 160])

    def enter(self):
        new_s = Scene(self.game)
        self.game.scene(new_s)

    def update(self):
        pass

    def clear(self):
        self.screen.fill([255, 255, 255])

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

    def run(self):
        self.event_listener()
        actions = self.actions.keys()
        for k in actions:
            if self.keydowns.get(k):
                self.actions.get(k)()


class Scene:

    actions = {}
    keydowns = {}

    score = 0

    ball = None
    paddle = None
    blocks = []

    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        ball = Ball()
        paddle = Paddle()
        blocks = []
        for i in range(7):
            blocks.append(Block([i * 50 + 20, 100]))

        self.register_action(pygame.K_LEFT, paddle.move_left)
        self.register_action(pygame.K_RIGHT, paddle.move_right)
        self.register_action(pygame.K_SPACE, ball.fire)
        self.register_action(pygame.K_ESCAPE, sys.exit)
        self.draw(ball=ball, paddle=paddle, blocks=blocks)

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

    def clear(self):
        self.screen.fill([0, 0, 0])

    def draw_image(self, i):
        self.screen.blit(i.image, i.position())

    def draw_text(self, text, position):
        font = pygame.font.Font(None, 20)
        text_object = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_object, position)

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

    def run(self):
        self.event_listener()
        actions = self.actions.keys()
        for k in actions:
            if self.keydowns.get(k):
                self.actions.get(k)()


class Game:
    _size = width, height = 400, 300
    _fps = 100

    s = None

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(self._size)
        self.screen = screen

    def scene(self, scene):
        self.s = scene

    def update(self):
        self.s.update()

    def draw(self, **kwargs):
        self.s.draw(kwargs)

    def run(self):
        while True:
            self.s.run()
            self.s.update()
            self.s.clear()
            self.s.draw()
            pygame.display.flip()
            time.sleep(1 / self._fps)


if __name__ == '__main__':
    g = Game()
    # s = Scene(g)
    s = Start(g)
    g.scene(s)
    g.run()
