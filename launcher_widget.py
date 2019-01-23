# -*- coding: utf-8 -*-

from constants import Path
from widget import Menu_widget, Text, Widget, Eventable_widget, Image_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

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


class Notif_widget(Menu_widget):
    pass


class Toast_widget(Widget):
    pass
