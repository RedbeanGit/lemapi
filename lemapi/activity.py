# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version__ = "0.1.0"


class Activity(object):
    def __init__(self, view):
        self.view = view
        self.events = []

    def update(self, deltatime):
        self.view.update()

    def sleep(self):
        for event in self.events:
            event.enable = False

    def wakeup(self):
        for event in self.events:
            event.enable = True

    def destroy(self):
        self.view.destroy()
