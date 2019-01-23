#!/usr/bin/env python
# -*- coding: utf-8 -*-

from activity import Desktop_activity
from api import stop_all_activities
from system_instance import Instance
from event_manager import Listener_manager
from gui import GUI
from util import exit
from view import Desktop_view

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import pygame
import os
import sys
import traceback

from pygame.locals import K_LCTRL, K_ESCAPE


def main():
    try:
        print("[INFO] [main] Lem Launcher started")
        pygame.init()

        Instance.gui = GUI()
        Instance.gui.create_root_surface()
        Instance.gui.load_images()

        Instance.listener_manager = Listener_manager()

        view = Desktop_view()
        view.init_widgets()

        Instance.activities.append(Desktop_activity(view))

        clock = pygame.time.Clock()

        while True:
            pygame.event.pump()
            deltatime = clock.tick() / 1000

            try:
                Instance.listener_manager.update()
                Instance.activities[-1].update(deltatime)
            except Exception:
                stop_all_activities()
                traceback.print_exc()

            Instance.gui.update()
    except Exception:
        print("[FATAL ERROR] [main] Something wrong happened!")
        pygame.quit()
        traceback.print_exc()


if __name__ == "__main__":
    dname = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(dname)
    sys.path.append(os.path.dirname(dname))
    main()
