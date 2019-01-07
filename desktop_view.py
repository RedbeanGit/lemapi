# -*- coding: utf -*-

from constants import Instance, Path
from layout import Layout
from util import read_json

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os


class Desktop_view(object):

    def __init__(self):
        self.widgets = []
        self.icons = []
        self.layout = Layout(read_json(os.path.join(Path.VIEWS, "desktop.json")))

    def init_widgets(self):
        pass
