import pygame
from paddle import Paddle
from block import Block
import scene.core
import scene.start


class EditScene(scene.core.CoreScene):

    level = 0

    ball = None
    paddle = None
    blocks = []

    def __init__(self, game):
        super(scene.core.CoreScene, self).__init__(game)

        paddle = Paddle()
        blocks = []

        self.register_action(pygame.K_SPACE, self.save)
        self.register_action(pygame.K_r, self.back)
        self.draw(paddle=paddle, blocks=blocks)

    def back(self):
        new_s = scene.start.StartScene(self.game)
        self.game.scene(new_s)

    def save(self):
        config = self.game.config
        level = config.get('level')

        blocks_array = []
        for i in self.blocks:
            blocks_array.append([i.x, i.y])

        level.append(blocks_array)
        self.back()
        # 不对关卡进行持久

    def draw(self, **kwargs):
        for i in kwargs.keys():
            if i == 'paddle':
                self.paddle = kwargs.get(i)
            if i == 'blocks':
                self.blocks = kwargs.get(i)

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

        self.draw_text('press space to save and return', [110, 20])

    def update(self):
        pass

    def listener_processor(self, event):
        super().listener_processor(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.blocks.append(Block(pos))
