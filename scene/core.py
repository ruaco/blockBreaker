# 打砖块游戏场景类
import pygame
import sys
from ball import Ball
from paddle import Paddle
from block import Block
from scene.base_scene import BaseScene
import scene.end_scene


class CoreScene(BaseScene):

    ball = None
    paddle = None
    blocks = []

    def __init__(self, game, level=0):
        super().__init__(game)
        self.level = level

        ball = Ball()
        paddle = Paddle()
        blocks = []
        for i in game.config.get('level')[self.level]:
            blocks.append(Block(i))

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
        blocks_exist = False
        if len(blocks) > 0:
            for i in blocks:
                if i.alive:
                    blocks_exist = blocks_exist or True
                    self.draw_image(i)
        if not blocks_exist:
            next_level = self.level + 1
            if len(self.game.config.get('level')) > next_level:
                new_s = CoreScene(self.game, next_level)
                self.game.scene(new_s)
            # todo 这里有一个Import Error
            # else:
            #     new_s = StartScene(self.game)
            #     self.game.scene(new_s)
        if ball.y+ball.height > self.game.height:
            ...
            new_s = scene.end_scene.EndScene(self.game, True)
            self.game.scene(new_s)

        self.draw_text('score: ' + str(self.score), [20, 20])

