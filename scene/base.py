import pygame
import sys
import util


class BaseScene:

    ball = None
    paddle = None
    blocks = []

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.actions = {}
        self.keydowns = {}

    def clear(self):
        self.screen.fill([0, 0, 0])

    def draw_image(self, i):
        self.screen.blit(i.image, i.position())

    def draw_text(self, text, position):
        font = pygame.font.Font(None, 20)
        text_object = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_object, position)

    def listener_processor(self, event):
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

    def event_listener(self):
        for event in pygame.event.get():
            self.listener_processor(event)

    def register_action(self, key, func):
        self.actions[key] = func

    def update(self):
        pass

    def draw(self, **kwargs):
        pass

    def run(self):
        self.event_listener()
        actions = self.actions.keys()
        for k in actions:
            if self.keydowns.get(k):
                self.actions.get(k)()
