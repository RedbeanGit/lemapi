# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

from os.path import join


class App(object):
    NAME = "Lem Launcher"
    GPIO_ENABLE = False


class Path(object):
    DATA = "data"
    IMAGES = join(DATA, "images")
    GUI = join(IMAGES, "gui")
    AUDIO = join(DATA, "audio")
    MUSIC = join(AUDIO, "music")
    GAMES = join("/", "home", "{user}", "games")
