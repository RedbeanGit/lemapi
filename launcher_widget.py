# -*- coding: utf-8 -*-

from constants import Path
from widget import Menu_widget, Text, Widget, Eventable_widget, Image_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from os.path import join


class App_widget(Menu_widget, Eventable_widget):

    DEFAULT_KWARGS = {
        "backgroundImage": join(Path.GUI, "app_frame.png"),
        "iconBorderImage": join(Path.GUI, "app_border.png"),
        "size": (300, 80)
    }

    def __init__(self, gui, pos, app, **kwargs):
        App_widget.updateDefaultKwargs(kwargs)
        self.app = app
        super().__init__(gui, pos, **kwargs)

    def initWidgets(self):
        w, h = self.kwargs["size"]
        self.addSubWidget("app_icon_image", Image_widget, (w * 0.25, h * 0.5), \
            self.app.get_icon_path(), size=(h * 0.8, h * 0.8), anchor=(0, 0))
        self.addSubWidget("app_border_image", Image_widget, (w * 0.25, h * 0.5), \
            self.kwargs["iconBorderImage"], size=(h * 0.8, h * 0.8), \
            anchor=(0, 0))
        self.addSubWidget("app_name_text", Text, (w * 0.75, h * 0.25), \
            self.app.get_name())
        self.addSubWidget("app_version_text", Text, (w * 0.75, h * 0.5), \
            "v" + self.app.get_version())


class Notif_widget(Menu_widget):
    pass


class Toast_widget(Widget):
    pass
