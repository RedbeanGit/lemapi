# -*- coding: utf-8 -*-

from lemapi.constants import App, Path
from lemapi.util import read_json

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
        print("[lemapi] [INFO] [GUI.create_root_surface] Creating display " \
            + "surface (800x480 manual)")
        self.root_surface = pygame.display.set_mode(App.SCREEN_SIZE)#, pygame.FULLSCREEN)
        pygame.display.set_caption(App.NAME)

    def load_images(self):
        print("[lemapi] [INFO] [GUI.load_images] Loading system images")
        images = read_json(os.path.join(Path.IMAGES, "resources.json"))
        if images:
            for image in images:
                self.load_image(os.path.join(Path.IMAGES, *image))

    def load_image(self, path):
        if os.path.exists(path):
            try:
                self.images[path] = pygame.image.load(path)
                print("[lemapi] [INFO] [GUI.load_image] Image '%s' loaded" % \
                    path)
            except Exception:
                print("[lemapi] [WARNING] [GUI.load_image] Something wrong " \
                    + "happened while loading '%s'" % path)
        else:
            print("[lemapi] [WARNING] [GUI.load_image] Image '%s' not found" % \
                path)

    def get_image(self, path, alpha = True):
        if path in self.images:
            if alpha:
                return self.images[path].convert_alpha()
            return self.images[path].convert()
        print("[lemapi] [WARNING] [GUI.get_image] Image '%s' not loaded!" % \
            path)
        return pygame.surface.Surface((16, 16))

    def update(self):
        pygame.display.update(self.updated_rect)
        self.updated_rect.clear()

    def draw_image(self, image, pos):
        if self.root_surface:
            self.root_surface.blit(image, pos)
            self.updated_rect.append((pos, image.get_size()))
        else:
            print("[lemapi] [WARNING] [GUI.draw_image] Can't draw any image ! No" \
                + " root surface created yet !")

    def draw_color(self, color, pos, size):
        if self.root_surface:
            rect = (pos, size)
            self.root_surface.fill(color, rect)
            self.updated_rect.append(rect)
        else:
            print("[lemapi] [WARNING] [GUI.draw_color] Can't apply any color ! " \
                + "No root surface created yet !")

    def draw_background_color(self, color):
        if self.root_surface:
            rect = ((0, 0), self.get_size())
            self.root_surface.fill(color)
            self.updated_rect.append(rect)
        else:
            print("[lemapi] [WARNING] [GUI.draw_background_color] Can't apply " \
                "any color ! No root surface created yet !")

    def draw_polygon(self, color, pos):
        if self.root_surface:
            x = min(pos, key=lambda p: p[0])[0]
            y = min(pos, key=lambda p: p[1])[1]
            w = max(pos, key=lambda p: p[0])[0] - x
            h = max(pos, key=lambda p: p[1])[1] - y
            pygame.draw.polygon(self.root_surface, color, pos)
            self.updated_rect.append(((x, y), (w, h)))
        else:
            print("[lemapi] [WARNING] [GUI.draw_polygon] Can't draw any polygon ! " \
                + "No root surface created yet !")

    def draw_line(self, color, pos1, pos2, width=1):
        if self.root_surface:
            x = min(pos1[0], pos2[0])
            y = min(pos1[1], pos2[1])
            w = max(pos1[0], pos2[0]) - x
            h = max(pos1[1], pos2[1]) - y
            pygame.draw.line(self.root_surface, color, pos1, pos2, width)
            self.updated_rect.append(((x, y), (w, h)))
        else:
            print("[lemapi] [WARNING] [GUI.draw_line] Can't draw any line ! " \
                + "No root surface created yet !")

    def get_size(self):
        if self.root_surface:
            return self.root_surface.get_size()
        return (0, 0)
