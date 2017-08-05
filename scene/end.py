import pygame
import sys
import scene.base
import scene.start


class EndScene(scene.base.BaseScene):

    def __init__(self, game, complete):
        super().__init__(game)
        self.complete = complete
        self.register_action(pygame.K_r, self.enter)
        self.register_action(pygame.K_q, sys.exit)

    def enter(self):
        new_s = scene.start.StartScene(self.game)
        self.game.scene(new_s)

    def draw(self):
        if self.complete:
            self.draw_text('mission completed!', [130, 120])
        else:
            self.draw_text('you failed~', [160, 120])
        self.draw_text('press R to return title scene to restart game', [70, 140])

    def update(self):
        pass
