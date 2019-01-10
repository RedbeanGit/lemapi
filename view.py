# -*- coding: utf -*-

from constants import Instance, Path
from layout import Layout
from util import read_json

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import collection


class View(object):
    def __init__(self):
        self.widgets = collection.OrderedDict()
        self.layout = None

    def load_layout(self, template_path):
        template = read_json()
        if template == None:
            print("[WARNING] [View.load_layout] None template")
        else:
            self.layout = Layout(template)

    def init_widgets(self):
        pass

    def add_widget(self, wname, wtype, pos, *wargs, **wkargs):
        if Instance.gui:
            if wname in self.widgets:
                self.widgets[wname].destroy()
            self.widgets[wname] = wtype(Instance.gui, pos, *wargs, **wkargs)

    def remove_widget(self, wname):
        if wname in self.widgets:
            self.widgets[wname].destroy()
            self.widgets.pop(wname)

    def update(self):
        for widget in tuple(self.widgets.values()):
            widget.update()

    def destroy(self):
        for widget in tuple(self.widgets.values()):
            widget.destroy()
        if Instance.view == self:
            Instance.view = None


class Desktop_view(View):
    def __init__(self):
        super().__init__()
        self.layout = self.load_layout(os.path.join(Path.VIEWS, "desktop.json"))

    def init_widgets(self):
        pass
