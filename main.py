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
        print("[lemapi] [INFO] [main] Defining working directory ...")
        define_working_directory()
        print("[lemapi] [INFO] [main] Initializing pygame ...")
        pygame.init()

        print("[lemapi] [INFO] [main] Creating system GUI ...")
        Instance.gui = GUI()
        Instance.gui.create_root_surface()

        print("[lemapi] [INFO] [main] Creating system Listener_manager ...")
        Instance.listener_manager = Listener_manager()
        print("[lemapi] [INFO] [main] Creating system Task_manager ...")
        Instance.task_manager = Task_manager()
        print("[lemapi] [INFO] [main] Creating system audio Player ...")
        Instance.audio_player = Player()
        Instance.audio_player.play()

        print("[lemapi] [INFO] [main] Creating first activity ...")
        view = Splash_view()
        view.init_widgets()
        Instance.activities.append(Splash_activity(view))

        clock = pygame.time.Clock()

        print("[lemapi] [INFO] [main] Init complete ! Starting system loop ...")
        while True:
            pygame.event.pump()
            deltatime = clock.tick() / 1000

            try:
                Instance.listener_manager.update()
                Instance.task_manager.update(deltatime)
                Instance.activities[-1].update(deltatime)
            except Exception:
                if Instance.app:
                    print("[lemapi] [WARNING] [main] " \
                    "'%s' has stopped working !" % Instance.app.get_name())

                traceback.print_exc()

            Instance.gui.update()
    except Exception:
        print("[FATAL ERROR] [main] Something wrong happened!")
        pygame.quit()
        traceback.print_exc()


def define_working_directory():
    dname = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(dname)
    sys.path.append(os.path.dirname(dname))


if __name__ == "__main__":
    main()
