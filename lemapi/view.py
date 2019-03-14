# -*- coding: utf -*-

from lemapi.api import get_gui
from lemapi.widget import Toast_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import collections
import random


class View(object):
    def __init__(self):
        self.widgets = collections.OrderedDict()
        self.toast = None
        self.init_widgets()

    def init_widgets(self):
        pass

    def add_widget(self, wname, wtype, pos, *wargs, **wkargs):
        if wname in self.widgets:
            self.widgets[wname].destroy()
        gui = get_gui()
        self.widgets[wname] = wtype(gui, pos, *wargs, **wkargs)

    def add_toast(self, message, **kwargs):
        self.toast = Toast_widget(get_gui(), (400, 400), message, **kwargs)

    def remove_widget(self, wname):
        if wname in self.widgets:
            self.widgets[wname].destroy()
            self.widgets.pop(wname)

    def remove_toast(self):
        if self.toast:
            self.toast.destroy()
            self.toast = None

    def update(self):
        for widget in tuple(self.widgets.values()):
            widget.update()

        if self.toast:
            self.toast.update()

    def updateEvent(self, event):
        for widget in tuple(self.widgets.values()):
            widget.onEvent(event)

    def destroy(self):
        for widget in tuple(self.widgets.values()):
            widget.destroy()
        self.widgets.clear()
