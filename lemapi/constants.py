# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

import sys
from os.path import join, dirname, abspath


class App(object):
    NAME = "LemAPI"
    GPIO_ENABLE = False
    RPI_ENV = False
    SCREEN_SIZE = (800, 480)
    SPLASH_ANIMATION = True
    VERSION = "0.2.0"
    DEFAULT_SETTINGS = {
        "sound_volume": 1,
        "theme_color": "white",
        "username": "LemAPI user",
        "custom_date": (0, 0, 0),
        "custom_time": (0, 0)
    }
    DEFAULT_APPS = ("Pyoro", "Robot", "Settings")
    THEME_COLORS = ("white", "blue", "green", "red", "magenta", "orange", "cyan", "yellow")


class Path(object):
    ROOT = dirname(abspath(sys.argv[0]))
    DATA = join(ROOT, "data")
    IMAGES = join(DATA, "images")
    AUDIO = join(DATA, "audio")
    MUSICS = join(AUDIO, "music")
    SOUNDS = join(AUDIO, "sounds")
    GAMES = join("/", "home", "{user}", "games")
    SAVES = join("/", "home", "{user}", "saves")


class GPIO(object):
    JOY_X = 0
    JOY_Y = 1
    JOY_BUTTON = 4
    BUTTON_A = 17
    BUTTON_B = 18
    BUTTON_X = 27
    BUTTON_Y = 22
