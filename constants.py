# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

import sys
from os.path import join, dirname, abspath


class App(object):
    NAME = "Lem Launcher"
    GPIO_ENABLE = False


class Path(object):
    ROOT = dirname(abspath(sys.argv[0]))
    DATA = join(ROOT, "data")
    IMAGES = join(DATA, "images")
    GUI = join(IMAGES, "gui")
    AUDIO = join(DATA, "audio")
    MUSIC = join(AUDIO, "music")
    GAMES = join("/", "home", "{user}", "games")
