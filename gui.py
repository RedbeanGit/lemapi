# -*- coding: utf-8 -*-

from constants import App

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import pygame


class GUI(object):

    def __init__(self):

        if not pygame.get_init():
            pygame.init()

        self.images = {}
        self.root_surface = None
        self.updated_rect = []
        self.view = None

    def create_root_surface(self):
        self.root_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(App.NAME)

    def load_images(self):
        pass

    def load_image(self, path):
        if os.path.exists(path):
            self.images = pygame.image.load(path)

    def get_image(self, path, alpha = True):
        if path in self.images:
            if alpha:
                return self.images[path].convert_alpha()
            return self.images[path].convert()
        return pygame.surface.Surface((16, 16))

    def update(self):
        pygame.display.update(self.updated_rect)
        self.updated_rect.clear()

    def draw_image(self, image, pos):
        if self.root_surface:
            self.root_surface.blit(image, pos)
            self.updated_rect.append((pos, image.get_size()))

    def get_size(self):
        if self.root_surface:
            return self.root_surface.get_size()
        return (0, 0)
