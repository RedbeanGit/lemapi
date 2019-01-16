# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version = "0.1.0"

from os.path import join


class App(object):
    NAME = "Lem Launcher"


class Path(object):
    DATA = "data"
    IMAGES = join(DATA, "images")
    GUI = join(IMAGES, "gui")
    VIEWS = join(DATA, "views")
    GAMES = join("/", "home", "{user}", "games")


class Instance(object):
    gui = None
    audio_player = None
    view = None
    backup_view = None
    app = None
    activity = None
    backup_activity = None
    event_manager = None
