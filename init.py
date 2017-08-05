import pygame
import time
from util import *
import scene.end


class Game:
    _size = width, height = 400, 300
    _fps = 100
    config = load_config_from_file()

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
    s = scene.end.StartScene(g)
    g.scene(s)
    g.run()
