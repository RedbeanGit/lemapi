# -*- coding: utf -*-

from api import get_gui
from constants import Path
from launcher_widget import App_group, Clock_widget, Splash_labyrinth
from util import read_json
from widget import Image_widget, Text
from launcher_widget import Toast_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import collections
import random


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

    def add_toast(self, message, **kwargs):
        name = "toast_%s_%s" % (message, random.random())
        if "view_id" in kwargs:
            kwargs.pop("view_id")
            
        self.widgets[name] = Toast_widget(get_gui(), (400, 400), message, \
            view_id=name, **kwargs)

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

        gui.load_image(os.path.join(Path.IMAGES, "splash", "labyrinth_part_1.png"))
        gui.load_image(os.path.join(Path.IMAGES, "splash", "labyrinth_part_2.png"))
        gui.load_image(os.path.join(Path.IMAGES, "splash", "labyrinth_part_3.png"))

        self.add_widget("labyrinth_widget", Splash_labyrinth, (w // 2, h // 2), \
            size=(h * 0.8, h * 0.8), anchor=(0, 0))

        path = os.path.join(Path.IMAGES, "splash", "lem_logo.png")
        gui.load_image(path)
        self.add_widget("title_image", Image_widget, (w // 2, h // 2), \
            path, size=(h * 0.4, h * 0.4), anchor=(0, 0), alphaChannel=False, \
            transparentColor=(0, 0, 0))
        self.widgets["title_image"].set_opacity(0)

        self.add_widget("loading_text", Text, (w // 2, h * 0.95), "Démarrage...", \
            anchor=(0, 0), fontSize=20, textColor=(75, 75, 75, 0))

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
