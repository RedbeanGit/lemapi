# -*- coding: utf-8 -*-

from constants import App, Path
from util import read_json

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import pygame


class GUI(object):
    def __init__(self):
        self.images = {}
        self.root_surface = None
        self.updated_rect = []

    def create_root_surface(self):
        self.root_surface = pygame.display.set_mode((800, 480))#, pygame.FULLSCREEN)
        pygame.display.set_caption(App.NAME)

    def load_images(self):
        images = read_json(os.path.join(Path.IMAGES, "resources.json"))
        if images:
            for image in images:
                self.load_image(os.path.join(Path.IMAGES, *image))

    def load_image(self, path):
        if os.path.exists(path):
            try:
                self.images[path] = pygame.image.load(path)
                print("[INFO] [GUI.load_image] Image '%s' loaded" % path)
            except Exception:
                pass
        else:
            print("[WARNING] [GUI.load_image] Image '%s' not found" % path)

    def get_image(self, path, alpha = True):
        if path in self.images:
            if alpha:
                return self.images[path].convert_alpha()
            return self.images[path].convert()
        print("[WARNING] [GUI.get_image] Image '%s' not loaded!" % path)
        return pygame.surface.Surface((16, 16))

    def update(self):
        pygame.display.update(self.updated_rect)
        self.updated_rect.clear()

    def draw_image(self, image, pos):
        if self.root_surface:
            self.root_surface.blit(image, pos)
            self.updated_rect.append((pos, image.get_size()))

    def draw_color(self, color, pos, size):
        if self.root_surface:
            rect = (pos, size)
            self.root_surface.fill(color, rect)
            self.updated_rect.append(rect)

    def draw_background_color(self, color):
        if self.root_surface:
            rect = ((0, 0), self.get_size())
            self.root_surface.fill(color)
            self.updated_rect.append(rect)

    def draw_polygon(self, color, pos):
        if self.root_surface:
            x = min(pos, key=lambda p: p[0])[0]
            y = min(pos, key=lambda p: p[1])[1]
            w = max(pos, key=lambda p: p[0])[0] - x
            h = max(pos, key=lambda p: p[1])[1] - y
            pygame.draw.polygon(self.root_surface, color, pos)
            self.updated_rect.append(((x, y), (w, h)))

    def draw_line(self, color, pos1, pos2, width=1):
        if self.root_surface:
            x = min(pos1[0], pos2[0])
            y = min(pos1[1], pos2[1])
            w = max(pos1[0], pos2[0]) - x
            h = max(pos1[1], pos2[1]) - y
            pygame.draw.line(self.root_surface, color, pos1, pos2, width)
            self.updated_rect.append(((x, y), (w, h)))

    def get_size(self):
        if self.root_surface:
            return self.root_surface.get_size()
        return (0, 0)
