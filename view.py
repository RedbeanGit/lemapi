# -*- coding: utf -*-

from api import get_gui
from constants import Path
from launcher_widget import App_group, Clock_widget
from util import read_json
from widget import Image_widget, Text

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


class Splash_view(View):
    def init_widgets(self):
        gui = get_gui()
        w, h = gui.get_size()

        labyrinth_path = os.path.join(Path.IMAGES, "splash", "labyrinth.png")
        gui.load_image(labyrinth_path)

        self.add_widget("labyrinth_image", Image_widget, (w // 2, h // 2), \
            labyrinth_path, size=(h * 0.8, h * 0.8), anchor=(0, 0), \
            alphaChannel=False)
        self.add_widget("title_text", Text, (w // 2, h // 2), "LemAPI", \
            anchor=(0, 0), fontSize=75, textColor=(255, 255, 255, 0))
        self.add_widget("loading_text", Text, (w // 2, h * 0.9), "Démarrage...", \
            anchor=(0, 0), fontSize=20, textColor=(75, 75, 75, 0))

        self.widgets["labyrinth_image"].set_opacity(0)

    def update(self):
        get_gui().draw_background_color((255, 255, 255))
        super().update()


class Desktop_view(View):
    def init_widgets(self):
        w, h = get_gui().get_size()
        bg_path = os.path.join(Path.IMAGES, "background", "white_degrade.jpg")

        self.add_widget("background_image", Image_widget, (w // 2, h // 2), \
            bg_path, size=(w, h), anchor=(0, 0))

        self.add_widget("app_group", App_group, (w, h // 2), anchor=(0, 0))

        self.add_widget("clock_widget", Clock_widget, (w * 0.1, h * 0.2), \
            anchor=(-1, 0))
