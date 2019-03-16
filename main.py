#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lemapi.api import stop_all_activities
from lemapi.audio import Player
from lemapi.constants import Path
from lemapi.event_manager import Listener_manager
from lemapi.gui import GUI
from lemapi.system_instance import Instance
from lemapi.task_manager import Task_manager
from lemapi.util import exit

from lemapi_desktop.activity import Splash_activity
from lemapi_desktop.view import Splash_view

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import pygame
import os
import sys
import traceback

from pygame.locals import K_LCTRL, K_ESCAPE


def main():
    # LemAPI init
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
        Instance.activities.append(Splash_activity(view))

        clock = pygame.time.Clock()
    except Exception:
        print("[lemapi] [FATAL ERROR] [main] Something wrong happened on boot!")
        traceback.print_exc()
        exit()

    # Loop
    print("[lemapi] [INFO] [main] Init complete ! An infinite loop is now" \
        +" running until the system stop")
    while True:
        pygame.event.pump()
        deltatime = clock.tick() / 1000

        # Listener manager update
        try:
            Instance.listener_manager.update()
        except Exception:
            if Instance.app:
                print("[lemapi] [WARNING] [main] " \
                    + "'%s' has stopped working " % Instance.app.get_name() \
                    + "on an event call!")
                traceback.print_exc()
            else:
                print("[lemapi] [FATAL ERROR] [main] LemAPI has stopped working" \
                    + " because of an event call!")
                traceback.print_exc()
                exit()

        # Task manager update
        try:
            Instance.task_manager.update(deltatime)
        except Exception:
            if Instance.app:
                print("[lemapi] [WARNING] [main] " \
                    + "'%s' has stopped working " % Instance.app.get_name() \
                    + "on a task call!")
                traceback.print_exc()
            else:
                print("[lemapi] [FATAL ERROR] [main] LemAPI has stopped working" \
                    + " because of a task call!")
                traceback.print_exc()
                exit()

        # Activity update
        try:
            Instance.activities[-1].update(deltatime)
        except Exception:
            if Instance.app:
                print("[lemapi] [WARNING] [main] " \
                    + "'%s' has stopped working " % Instance.app.get_name() \
                    + "while updating its current activity!")
                traceback.print_exc()
            else:
                print("[lemapi] [FATAL ERROR] [main] LemAPI has stopped working" \
                    + " while updating the current activity!")
                traceback.print_exc()
                exit()

        # Display update
        Instance.gui.update()


def define_working_directory():
    dname = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(dname)


if __name__ == "__main__":
    print("[lemapi] [INFO] Starting LemAPI...")
    main()
