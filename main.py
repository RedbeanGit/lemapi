#!/usr/bin/env python
# -*- coding: utf-8 -*-

from activity import Splash_activity
from api import stop_all_activities
from audio import Player
from event_manager import Listener_manager
from gui import GUI
from system_instance import Instance
from task_manager import Task_manager
from util import exit
from view import Splash_view

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

        Instance.listener_manager = Listener_manager()
        Instance.task_manager = Task_manager()

        Instance.audio_player = Player()
        Instance.audio_player.play()

        view = Splash_view()
        view.init_widgets()
        Instance.activities.append(Splash_activity(view))

        clock = pygame.time.Clock()

        while True:
            pygame.event.pump()
            deltatime = clock.tick() / 1000

            try:
                Instance.listener_manager.update()
                Instance.task_manager.update(deltatime)
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
