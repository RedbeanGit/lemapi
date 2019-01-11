#!/usr/bin/env python
# -*- coding: utf-8 -*-

from activity import Desktop_activity
from constants import Instance
from event_manager import Event_manager
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

        Instance.event_manager = Event_manager()
        Instance.event_manager.add_keyboard_listener(exit, K_LCTRL, \
            modifiers = [K_ESCAPE])

        Instance.view = Desktop_view()
        Instance.view.init_widgets()

        Instance.activity = Desktop_activity(Instance.view)

        clock = pygame.time.Clock()

        while True:
            pygame.event.pump()
            deltatime = clock.tick()

            Instance.event_manager.update()
            if Instance.app:
                Instance.app.update(deltatime)
            else:
                Instance.activity.update(deltatime)
            Instance.gui.update()
    except Exception:
        print("[FATAL ERROR] [main] Something wrong happened!")
        pygame.quit()
        traceback.print_exc()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    main()
