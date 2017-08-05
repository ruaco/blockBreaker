import pygame
import sys
import scene.base
import scene.core
import scene.edit


class StartScene(scene.base.BaseScene):

    def __init__(self, game):
        super().__init__(game)
        self.register_action(pygame.K_r, self.enter)
        self.register_action(pygame.K_e, self.edit)
        self.register_action(pygame.K_q, sys.exit)

    def enter(self):
        new_s = scene.core.CoreScene(self.game, 0)
        self.game.scene(new_s)

    def edit(self):
        new_s = scene.edit.EditScene(self.game)
        self.game.scene(new_s)

    def draw(self):
        self.draw_text('press R to start game', [130, 120])
        self.draw_text('press E to add level', [130, 140])
        self.draw_text('press Q to exit game', [132, 160])

    def update(self):
        pass
