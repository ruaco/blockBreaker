import pygame
import sys
from scene.base_scene import BaseScene
from scene.core_scene import CoreScene


class StartScene(BaseScene):

    def __init__(self, game):
        super().__init__(game)
        self.register_action(pygame.K_r, self.enter)
        self.register_action(pygame.K_q, sys.exit)

    def enter(self):
        new_s = CoreScene(self.game, 0)
        self.game.scene(new_s)

    def draw(self):
        self.draw_text('press R to start game', [130, 120])
        self.draw_text('exit game', [160, 140])

    def update(self):
        pass
