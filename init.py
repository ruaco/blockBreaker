import pygame
import sys
import time
from util import log, rect_intersects


size = width, height = 400, 300


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


class Game:
    actions = {}
    keydowns = {}
    _fps = 100
    ball = None
    paddle = None
    blocks = []
    score = 0

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
            if event.type == pygame.QUIT:
                sys.exit()

    def slow(self):
        self._fps = 0.5

    def fast(self):
        self._fps = 150

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
    g.register_action(pygame.K_f, g.slow)
    g.register_action(pygame.K_j, g.fast)
    g.draw(ball=ball, paddle=paddle, blocks=blocks)

    g.run()

if __name__ == '__main__':
    __main()
