# -*- coding: utf -*-

from api import get_gui
from constants import Path
from util import read_json
from widget import Image_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import collections


class View(object):
    def __init__(self):
        self.widgets = collections.OrderedDict()
        self.init_widgets()

    def init_widgets(self):
        pass

    def add_widget(self, wname, wtype, pos, *wargs, **wkargs):
        if wname in self.widgets:
            self.widgets[wname].destroy()
        gui = get_gui()
        self.widgets[wname] = wtype(gui, pos, *wargs, **wkargs)

    def remove_widget(self, wname):
        if wname in self.widgets:
            self.widgets[wname].destroy()
            self.widgets.pop(wname)

    def update(self):
        for widget in tuple(self.widgets.values()):
            widget.update()

    def updateEvent(self, event):
        for widget in tuple(self.widgets.values()):
            widget.onEvent(event)

    def destroy(self):
        for widget in tuple(self.widgets.values()):
            widget.destroy()
        self.widgets.clear()


class Desktop_view(View):
    def __init__(self):
        super().__init__()

    def init_widgets(self):
        w, h = get_gui().get_size()
        bg_path = os.path.join(Path.IMAGES, "background", "white_degrade.jpg")
        self.add_widget("background_image", Image_widget, (w // 2, h // 2), \
            bg_path, size=(w, h), anchor=(0, 0))
