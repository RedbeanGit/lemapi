# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

from os.path import join
from enumeration import Enum


class App(Enum):
    NAME = "Lem Launcher"


class Path(Enum):
    DATA = "data"
    IMAGES = join(Path.DATA, "images")
    GUI = join(Path.IMAGES, "gui")
    VIEWS = join(Path.DATA, "views")
    GAMES = join("/", "home", "pi", "games")


class Instance(object):
    gui = None
    audio_player = None
    view = None
    app = None
    activity = None
    event_manager = None
