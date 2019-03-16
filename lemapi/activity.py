# -*- coding: utf-8 -*-

from lemapi.event_manager import Listener_manager

__author__ = "Julien Dubois"
__version__ = "0.1.0"


class Activity(object):
    def __init__(self, view):
        self.view = view
        self.listener_manager = Listener_manager()

    def update(self, deltatime):
        self.listener_manager.update()
        self.view.update()

    def sleep(self):
        self.listener_manager.enable = False

    def wakeup(self):
        self.listener_manager.enable = True

    def destroy(self):
        self.view.destroy()
        self.listener_manager.enable = False
        self.listener_manager.clear()
