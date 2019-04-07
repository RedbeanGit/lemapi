# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import datetime
import math
import time

from lemapi.api import get_task_manager, get_view, get_listener_manager
from lemapi.constants import Path
from lemapi.task_manager import Analog_task_delay
from lemapi.util import rotate_image, resize_image
from lemapi.widget import Menu_widget, Text, Widget, Eventable_widget, Image_widget

from os.path import join


class App_widget(Menu_widget, Eventable_widget):

    DEFAULT_KWARGS = {
        "size": (300, 80)
    }

    def __init__(self, gui, pos, app, **kwargs):
        App_widget.updateDefaultKwargs(kwargs)
        self.app = app

        super().__init__(gui, pos, **kwargs)
        Eventable_widget.__init__(self, gui, pos, **kwargs)

    def initWidgets(self):
        w, h = self.kwargs["size"]
        self.gui.load_image(self.app.get_icon_path())

        self.addSubWidget("app_icon_image", Image_widget, (w * 0.25, h * 0.5), \
            self.app.get_icon_path(), size=(h * 0.75, h * 0.75), anchor=(0, 0))
        self.addSubWidget("app_name_text", Text, (w * 0.5, h * 0.25), \
            self.app.get_name(), textColor=(50, 50, 50))
        self.addSubWidget("app_version_text", Text, (w * 0.5, h * 0.6), \
            "v" + self.app.get_version(), textColor=(50, 50, 50), fontSize=16)

    def onEvent(self, event):
        super().onEvent(event)
        Eventable_widget.onEvent(self, event)


class Splash_labyrinth(Widget):

    DEFAULT_KWARGS = {
        "size": (380, 380),
        "labyrinthPart1": join(Path.IMAGES, "splash", "labyrinth_part_1.png"),
        "labyrinthPart2": join(Path.IMAGES, "splash", "labyrinth_part_2.png"),
        "labyrinthPart3": join(Path.IMAGES, "splash", "labyrinth_part_3.png")
    }

    def __init__(self, gui, pos, **kwargs):
        Splash_labyrinth.updateDefaultKwargs(kwargs)
        self.angle = 0
        self.backgrounds = []
        self.last_time = time.time()
        self.rotate = False

        super().__init__(gui, pos, **kwargs)
        self.load_backgrounds()

    def load_backgrounds(self):
        self.backgrounds.append(resize_image(self.gui.get_image( \
            self.kwargs["labyrinthPart1"]), self.kwargs["size"]))
        self.backgrounds.append(resize_image(self.gui.get_image( \
            self.kwargs["labyrinthPart2"]), self.kwargs["size"]))
        self.backgrounds.append(resize_image(self.gui.get_image( \
            self.kwargs["labyrinthPart3"]), self.kwargs["size"]))

    def update(self):
        if self.backgrounds:
            if self.rotate:
                elapsed = time.time() - self.last_time
                self.angle += elapsed * 250

            w, h = self.kwargs["size"]

            for i in range(3):
                x, y = self.getRealPos()
                if i % 2:
                    surface = rotate_image(self.backgrounds[i], int(self.angle))
                else:
                    surface = rotate_image(self.backgrounds[i], -int(self.angle))
                sw, sh = surface.get_size()
                x -= (sw - w) / 2
                y -= (sh - h) / 2
                self.gui.draw_image(surface, (x, y))
            self.last_time = time.time()
        super().update()


class App_group(Eventable_widget):

    DEFAULT_KWARGS = {
        "size": (600, 600),
        "nbAppVisible": 3,
        "backgroundImage": join(Path.IMAGES, "labyrinth", "{theme_color}.png")
    }

    def __init__(self, gui, pos, **kwargs):
        App_group.updateDefaultKwargs(kwargs)
        self.app_widgets = []
        self.background = None
        self.angle = 1
        self.last_mouse_pos = []

        super().__init__(gui, pos, **kwargs)
        self.load_background()

    def load_background(self):
        self.background = resize_image(self.gui.get_image( \
            self.kwargs["backgroundImage"]), self.kwargs["size"])

    def get_delta_angle(self):
        return 0.5 / self.kwargs["nbAppVisible"]

    def get_current_app_widget(self):
        index = round((1 - self.angle) / self.get_delta_angle())
        return self.app_widgets[index]

    def reset_angle(self):
        app_index = math.ceil(len(self.app_widgets) / 2)
        self.angle = app_index * self.get_delta_angle() + 1/2
        print("[lemapi] [INFO] [App_group.reset_angle] Angle defined to %s radians" % \
            self.angle)

    def next_app(self):
        delta_angle = self.get_delta_angle()

        if self.angle > 1:
            self.angle = 1
        elif self.angle < 1 - (len(self.app_widgets) - 1) * delta_angle:
            self.angle = 1 - (len(self.app_widgets) - 1) * delta_angle

        app_index = math.ceil((1 - self.angle) / delta_angle)
        old_angle, self.angle = self.angle, 1 - delta_angle * app_index

        if old_angle == self.angle:
            if app_index < len(self.app_widgets) - 1:
                self.angle -= delta_angle

    def previous_app(self):
        delta_angle = self.get_delta_angle()

        if self.angle > 1:
            self.angle = 1
        elif self.angle < 1 - (len(self.app_widgets) - 1) * delta_angle:
            self.angle = 1 - (len(self.app_widgets) - 1) * delta_angle

        app_index = math.floor((1 - self.angle) / delta_angle)
        old_angle, self.angle = self.angle, 1 - delta_angle * app_index

        if old_angle == self.angle:
            if app_index > 0:
                self.angle += delta_angle

    def add_app_widget(self, app_widget):
        if isinstance(app_widget, App_widget):
            self.app_widgets.append(app_widget)

    def remove_app_widget(self, app_widget):
        if app_widget in self.app_widgets:
            self.app_widgets.remove(app_widget)

    def update(self):
        if self.background:
            self.update_background()
        self.update_app_widgets()
        super().update()

    def update_app_widgets(self):
        delta_angle = self.get_delta_angle()
        radius = min(self.kwargs["size"]) / 2
        sx, sy = self.getRealPos()
        w, h = self.kwargs["size"]
        sx, sy = sx + w / 2, sy + h / 2

        for index, app_widget in enumerate(self.app_widgets):
            x = math.cos((self.angle + index * delta_angle) * math.pi) * radius
            y = math.sin((self.angle + index * delta_angle) * math.pi) * radius
            app_widget.setPos((sx + x, sy + y))

    def update_background(self):
        x, y = self.getRealPos()
        w, h = self.kwargs["size"]
        surface = rotate_image(self.background, -self.angle * 180)

        sw, sh = surface.get_size()
        x -= (sw - w) / 2
        y -= (sh - h) / 2
        self.gui.draw_image(surface, (x, y))

    def update_angle(self):
        if self.clicked and self.last_mouse_pos:
            try:
                x, y = self.getRealPos()
                dy = self.lastEvent.pos[1] - self.last_mouse_pos[1]
                dx = self.lastEvent.pos[0] - x + self.kwargs["size"][0] / 2
                self.angle -= math.asin(dy / dx / math.pi)

                delta_angle = self.get_delta_angle()
                min_angle = 1 - (len(self.app_widgets) - 1) * delta_angle
                max_angle = 1

                if self.angle > max_angle:
                    self.angle = max_angle
                elif self.angle < min_angle:
                    self.angle = min_angle
            except ValueError:
                print("[lemapi] [WARNING] [App_group.update_angle] Bad position" \
                    + " (math domain error)")
            self.last_mouse_pos = list(self.lastEvent.pos)

    def onHover(self):
        self.update_angle()
        super().onHover()

    def onEndHover(self):
        self.update_angle()
        super().onEndHover()

    def onClick(self):
        self.last_mouse_pos = list(self.lastEvent.pos)
        super().onClick()

    def onEndClick(self):
        self.last_mouse_pos = []
        super().onEndClick()

    def click_app(self):
        app = self.get_current_app_widget()
        app.onClick()
        app.onEndClick()


class Clock_widget(Text):

    DEFAULT_KWARGS = {
        "fontSize": 70,
        "bold": True,
        "textColor": (100, 100, 100, 255)
    }

    def __init__(self, gui, pos, **kwargs):
        Clock_widget.updateDefaultKwargs(kwargs)
        super().__init__(gui, pos, "00:00", **kwargs)

    def update(self):
        dt = datetime.datetime.now()
        self.text = "%02d:%02d" % (dt.hour, dt.minute)
        super().update()


class App_descriptor(Menu_widget):

    DEFAULT_KWARGS = {
        "size": (150, 150)
    }

    def __init__(self, gui, pos, app, **kwargs):
        App_descriptor.updateDefaultKwargs(kwargs)
        super().__init__(gui, pos, **kwargs)

        self.app = app

    def initWidgets(self):
        w, h = self.kwargs["size"]
        self.addSubWidget("title_text", Text, (w*0.5, h*0.05), app.get_name(), \
            anchor=(0, -1))