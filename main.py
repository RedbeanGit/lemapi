#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import Instance
from desktop_view import Desktop_view
from gui import GUI

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import os
import sys


def main():
    try:
        Instance.gui = GUI()
        Instance.gui.create_root_surface()
        Instance.gui.load_images()

        Instance.view = Desktop_view()
        Instance.view.init_widgets()

        while True:
            pass

    except Exception:
        pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    main()
