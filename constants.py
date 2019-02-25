# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

import sys
from os.path import join, dirname, abspath


class App(object):
    NAME = "Lem Launcher"
    GPIO_ENABLE = False
    SCREEN_SIZE = (800, 480)


class Path(object):
    ROOT = dirname(abspath(sys.argv[0]))
    DATA = join(ROOT, "data")
    IMAGES = join(DATA, "images")
    GUI = join(IMAGES, "gui")
    AUDIO = join(DATA, "audio")
    MUSIC = join(AUDIO, "music")
    GAMES = join("/", "home", "{user}", "games")


class GPIO(object):
    JOY_X = 0
    JOY_Y = 1
    JOY_BUTTON = 4
    BUTTON_A = 17
    BUTTON_B = 18
    BUTTON_X = 27
    BUTTON_Y = 22
