# -*- coding: utf-8 -*-

from util import exit

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from pygame import event
from pygame.locals import QUIT, KEYDOWN, KEYUP

class Event_manager(object):
    def __init__(self):
        self.listeners = {}
        self.keys_down = []

    def add_keyboard_listener(self, fct, key, *args, modifiers = [], **kwargs):
        self.listeners[fct] = {
            "keys": [key] + modifiers,
            "args": args,
            "kwargs": kwargs
        }

    def remove_listener_by_function(self, fct):
        if fct in self.listeners:
            self.listeners.pop(fct)

    def remove_listener_by_key(self, key):
        for fct, infos in tuple(self.listeners.items()):
            if key in infos["keys"]:
                self.listeners.pop(fct)

    def remove_key(self, fct, key):
        if fct in self.listeners:
            if key in self.listeners[fct]["keys"]:
                self.listeners[fct]["keys"].remove(key)

    def update(self):
        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                self.keys_down.append(e.key)
            elif e.type == KEYUP:
                if e.key in self.keys_down:
                    self.keys_down.remove(e.key)
        self.update_listeners()

    def has_keys_down(self, keys):
        for key in keys:
            if key not in self.keys_down:
                return False
        return True

    def update_listeners(self):
        for fct, infos in tuple(self.listeners.items()):
            if self.has_keys_down(infos["keys"]):
                fct(*infos["args"], **infos["kwargs"])