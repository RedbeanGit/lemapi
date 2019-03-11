# -*- coding: utf-8 -*-

from lemapi.api import get_view
from lemapi.constants import GPIO, App
from lemapi.util import exit

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import gpiozero
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, JOYBUTTONDOWN, JOYBUTTONUP, \
    JOYAXISMOTION


class Listener_manager(object):
    def __init__(self):
        self.listeners = []
        self.km = Keyboard_manager(self)
        self.cm = Control_manager(self)

    def add_listener(self, event, type, *values):
        self.listeners.append((event, type, values))

    def clear(self):
        self.listeners.clear()

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            get_view().updateEvent(event)
        self.km.update()
        self.cm.update()


class Keyboard_manager(object):
    def __init__(self, listener_manager):
        self.lm = listener_manager
        self.current_states = []

    def add_key_down_event(self, event, key, *modifiers, copy=True):
        if copy:
            event = event.get_copy()
        self.lm.add_listener(event, KEYDOWN, key, *modifiers)

    def add_key_up_event(self, event, key, *modifiers, copy=True):
        if copy:
            event = event.get_copy()
        self.lm.add_listener(event, KEYUP, key, *modifiers)

    def update(self):
        pressed = pygame.key.get_pressed()
        for event, type, values in self.lm.listeners:

            if type == KEYDOWN:
                if Keyboard_manager.has_all_key_pressed(values, pressed):
                    if not event.obsolete:
                        event.call()
                else:
                    event.obsolete = False

            elif type == KEYUP:
                if Keyboard_manager.has_all_key_released(values, pressed):
                    if not event.obsolete:
                        event.call()
                else:
                    event.obsolete = False

    @staticmethod
    def has_all_key_pressed(pressed_keys, all_keys):
        for key in pressed_keys:
            if not all_keys[key]:
                return False
        return True

    @staticmethod
    def has_all_key_released(released_keys, all_keys):
        for key in released_keys:
            if all_keys[key]:
                return False
        return True


class Control_manager(object):
    def __init__(self, listener_manager):
        self.lm = listener_manager

        if App.GPIO_ENABLE:
            self.joystick = {
                "joy_x": gpiozero.MCP3008(GPIO.JOY_X),
                "joy_y": gpiozero.MCP3008(GPIO.JOY_Y),
            }

            self.buttons = {
                "button_joy": gpiozero.Button(GPIO.JOY_BUTTON),
                "button_a": gpiozero.Button(GPIO.BUTTON_A),
                "button_b": gpiozero.Button(GPIO.BUTTON_B),
                "button_x": gpiozero.Button(GPIO.BUTTON_X),
                "button_y": gpiozero.Button(GPIO.BUTTON_Y)
            }

            self.current_states = {
                "joy_x": 0,
                "joy_y": 0,
            }
        else:
            self.joystick = {}
            self.buttons = {}
            self.current_states = {}

    def add_button_pressed_event(self, event, button, *modifiers, copy=True):
        if copy:
            event = event.get_copy()
        self.lm.add_listener(event, JOYBUTTONDOWN, button, *modifiers)

    def add_button_released_event(self, event, button, *modifiers, copy=True):
        if copy:
            event = event.get_copy()
        self.lm.add_listener(event, JOYBUTTONUP, button, *modifiers)

    def add_joy_motion_event(self, event, copy=True):
        if copy:
            event = event.get_copy()
        self.lm.add_listener(event, JOYAXISMOTION)

    def update(self):
        if App.GPIO_ENABLE:
            pressed = self.get_pressed_buttons()
            for event, type, values in self.lm.listeners:

                if type == JOYAXISMOTION:
                    x = self.joystick["joy_x"].value * 2 - 1
                    y = self.joystick["joy_y"].value * 2 - 1
                    if x != self.current_states["joy_x"] \
                        or y != self.current_states["joy_y"]:
                        event.call(x, y, self.current_states["joy_x"], \
                            self.current_states["joy_y"])

                elif type == JOYBUTTONDOWN:
                    if Control_manager.has_all_button_pressed(pressed, values):
                        if not event.obsolete:
                            event.call()
                    else:
                        event.obsolete = False

                elif type == JOYBUTTONUP:
                    if Control_manager.has_all_button_released(pressed, values):
                        if not event.obsolete:
                            event.call()
                    else:
                        event.obsolete = False

            for name in ("joy_x", "joy_y"):
                self.current_states[name] = self.joystick[name].value * 2 - 1

    def get_pressed_buttons(self):
        return [name for name, button in self.buttons.items() if \
            button.is_pressed]

    @staticmethod
    def has_all_button_pressed(seq, subseq):
        for item in subseq:
            if item not in seq:
                return False
        return True

    @staticmethod
    def has_all_button_released(seq, subseq):
        for item in subseq:
            if item in seq:
                return False
        return True


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

    def get_copy(self):
        return Event(self.fct, *self.args, **self.kwargs)
