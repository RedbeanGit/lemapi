# -*- coding: utf-8 -*-

from constants import Path
from widget import Menu_widget, Text, Widget, Eventable_widget, Image_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import datetime
import math
from os.path import join


class App_widget(Menu_widget, Eventable_widget):

    DEFAULT_KWARGS = {
        "backgroundImage": join(Path.GUI, "app_frame.png"),
        "backgroundBorderSize": 30,
        "iconBorderImage": join(Path.GUI, "app_border.png"),
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
        self.addSubWidget("app_border_image", Image_widget, (w * 0.25, h * 0.5), \
            self.kwargs["iconBorderImage"], size=(h * 0.8, h * 0.8), \
            anchor=(0, 0), borderSize=10)
        self.addSubWidget("app_name_text", Text, (w * 0.5, h * 0.25), \
            self.app.get_name(), textColor=(50, 50, 50))
        self.addSubWidget("app_version_text", Text, (w * 0.5, h * 0.6), \
            "v" + self.app.get_version(), textColor=(50, 50, 50), fontSize=16)

    def onEvent(self, event):
        super().onEvent(event)
        Eventable_widget.onEvent(self, event)


class App_group(Eventable_widget):

    DEFAULT_KWARGS = {
        "size": (600, 600),
        "nbAppVisible": 3
    }

    def __init__(self, gui, pos, **kwargs):
        App_group.updateDefaultKwargs(kwargs)
        self.app_widgets = []
        self.visible_app_index = 0
        self.angle = 1
        self.last_mouse_pos = []

        super().__init__(gui, pos, **kwargs)

    def add_app_widget(self, app_widget):
        if isinstance(app_widget, App_widget):
            self.app_widgets.append(app_widget)

    def remove_app_widget(self, app_widget):
        if app_widget in self.app_widgets:
            self.app_widgets.remove(app_widget)

    def update(self):
        angle_app = 1 / 2 / self.kwargs["nbAppVisible"]
        radius = min(self.kwargs["size"]) / 2
        visible_apps = self.app_widgets[self.visible_app_index : \
            self.visible_app_index + self.kwargs["nbAppVisible"]]
        sx, sy = self.pos

        for index, app_widget in enumerate(visible_apps):
            x = math.cos((self.angle + index * angle_app) * math.pi) * radius
            y = -math.sin((self.angle + index * angle_app) * math.pi) * radius
            app_widget.setPos((x + sx, y + sy))

    def update_angle(self):
        if self.clicked and self.last_mouse_pos:
            self.angle += math.asin((self.lastEvent.pos[1] - \
                self.last_mouse_pos[1]) / abs(self.lastEvent.pos[0] - \
                self.pos[0]) / math.pi)
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


class Clock_widget(Text):

    DEFAULT_KWARGS = {
        "fontSize": 70,
        "bold": True,
        "textColor": (100, 100, 100, 110)
    }

    def __init__(self, gui, pos, **kwargs):
        Clock_widget.updateDefaultKwargs(kwargs)
        super().__init__(gui, pos, "00:00", **kwargs)

    def update(self):
        dt = datetime.datetime.now()
        self.text = "%s:%s" % (dt.hour, dt.minute)
        super().update()


class Notif_widget(Menu_widget):
    pass


class Toast_widget(Widget):
    pass
