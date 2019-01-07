# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

import os
from enumeration import Enum


class App(Enum):
    NAME = "Lem Launcher"


class Path(Enum):
    DATA = "data"
    IMAGES = os.path.join(Path.DATA, "images")
    GUI = os.path.join(Path.IMAGES, "gui")
    VIEWS = os.path.join(Path.DATA, "views")


class Instance(object):
    gui = None
    audio_player = None
    view = None
