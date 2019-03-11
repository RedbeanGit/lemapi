# -*- coding: utf-8 -*-

from lemapi_desktop.widget import App_group, Clock_widget, Splash_labyrinth, \
    Toast_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os

from lemapi.api import get_gui
from lemapi.constants import Path
from lemapi.util import read_json
from lemapi.view import View
from lemapi.widget import Image_widget, Text


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
