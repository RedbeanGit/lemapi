# -*- coding: utf-8 -*-

from util import exit

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from api import get_view
from pygame import event
from pygame.locals import QUIT, KEYDOWN, KEYUP


class Listener_manager(object):
    def __init__(self):
        self.listeners = {}
        self.keys_down = []
        self.keys_up = []

    def add_key_down_event(self, event, key, *modifiers):
        self.listeners[event] = (KEYDOWN, (key,) + modifiers)

    def add_key_up_event(self, event, key, *modifiers):
        self.listeners[event] = (KEYUP, (key,) + modifiers)

    def remove_event(self, event):
        if event in self.listeners:
            self.listeners.pop(event)

    def remove_all_events(self):
        self.listeners.clear()

    def update(self):
        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key in self.keys_up:
                    self.keys_up.remove(e.key)
                self.keys_down.append(e.key)
            elif e.type == KEYUP:
                if e.key in self.keys_down:
                    self.keys_down.remove(e.key)
                self.keys_up.append(e.key)
            get_view().updateEvent(e)
        self.update_listeners()

    @staticmethod
    def has_good_keys(check_keys, all_keys):
        for key in check_keys:
            if key not in all_keys:
                return False
        return True

    def update_listeners(self):
        for event, (etype, einfos) in tuple(self.listeners.items()):
            if etype == KEYDOWN:
                if self.has_good_keys(einfos, self.keys_down):
                    if not event.obsolete:
                        event.call()
                else:
                    event.obsolete = False
            elif etype == KEYUP:
                if self.has_good_keys(einfos, self.keys_up):
                    if not event.obsolete:
                        event.call()
                else:
                    event.obsolete = False


class Event(object):
    def __init__(self, fct, *args, **kwargs):
        self.fct = fct
        self.args = args
        self.kwargs = kwargs
        self.obsolete = False
        self.enable = True

    def call(self, *nargs, **nkwargs):
        self.obsolete = True

        if self.enable:
            self.fct(*nargs, *self.args, **nkwargs, **self.kwargs)
