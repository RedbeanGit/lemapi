# -*- coding: utf-8 -*-

from lemapi.system_instance import Instance

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import copy
import os
import sys
import traceback


def start_activity(activity):
    print("[lemapi] [INFO] [start_activity] Sleeping %s" % \
        Instance.activities[-1])
    Instance.activities[-1].sleep()
    Instance.activities.append(activity)


def stop_activity():
    if len(Instance.activities) > 1:
        print("[lemapi] [INFO] [stop_activity] Destroying activity %s" % \
            Instance.activities[-1])
        try:
            Instance.activities.pop().destroy()
            Instance.activities[-1].wakeup()
        except Exception:
            print("[lemapi] [WARNING] [stop_activity] Something wrong happened " \
                + "while stopping an activity")
            traceback.print_exc()
    else:
        print("[lemapi] [WARNING] [stop_activity] Unable to destroy " \
            + "Desktop_activity (main activity)")


def stop_all_activities():
    while len(Instance.activities) > 1:
        print("[lemapi] [INFO] [stop_activity] Destroying activity %s" % \
            Instance.activities[-1])
        try:
            activity = Instance.activities.pop()
            print("[lemapi] [INFO] [stop_all_activities] Destroying activity %s" \
                % activity)
            activity.destroy()
        except Exception:
            print("[lemapi] [WARNING] [stop_all_activities] Something wrong " \
                + "happened while stopping an activity")
            traceback.print_exc()
    Instance.activities[0].wakeup()


def get_gui():
    from lemapi.gui import GUI

    if not Instance.gui:
        Instance.gui = GUI()
    return Instance.gui


def get_listener_manager():
    return Instance.activities[-1].listener_manager


def get_global_listener_manager():
    from lemapi.event_manager import Listener_manager

    if not Instance.listener_manager:
        Instance.listener_manager = Listener_manager()
    return Instance.listener_manager


def get_task_manager():
    from lemapi.task_manager import Task_manager

    if not Instance.task_manager:
        Instance.task_manager = Task_manager()
    return Instance.task_manager


def get_activity():
    return Instance.activities[-1]


def get_view():
    return Instance.activities[-1].view


def get_audio_player():
    from lemapi.audio import Player

    if not Instance.audio_player:
        Instance.audio_player = Player()
        Instance.audio_player.play()
    return Instance.audio_player


def restart_app():
    if Instance.app:
        stop_all_activities()
        Instance.app.reload()
        Instance.app.run()
    else:
        print("[lemapi] [WARNING] [restart_app] No app currently running!")


def start_app(app):
    if Instance.app:
        print("[lemapi] [INFO] [run_app] Stopping app '%s'" % Instance.app.get_name())
        Instance.app.exit()

    print("[lemapi] [INFO] [run_app] Running app '%s'" % app.get_name())
    Instance.app = app
    app.load()
    app.run()


def stop_app():
    if Instance.app:
        Instance.app.exit()
        Instance.app = None
    else:
        print("[lemapi] [INFO] [stop_app] No app to stop")


def stop_audio_player():
    if Instance.audio_player:
        Instance.audio_player.stop()
    else:
        print("[lemapi] [INFO] [stop_audio_player] No player to stop")


def get_app_id():
    if Instance.app:
        return Instance.app.id
    return 0


def get_app_path(app_id=None):
    from lemapi.application import Application
    from lemapi.constants import Path

    if app_id == 0:
        return Path.ROOT
    if app_id == None and Instance.app:
        app_id = Instance.app.id
    if app_id <= len(Application.apps) and app_id > 0:
        return Application.apps[app_id - 1].path
    else:
        print("[lemapi] [WARNING] [get_app_path] No app with id=%s found!" % \
            app_id)


def force_view_update():
    Instance.activities[-1].view.update()
    Instance.gui.update()


def request_keyboard():
    from lemapi.constants import App
    from lemapi.widget import Virtual_keyboard

    view = get_view()

    if "<system>_virtual_keyboard" not in view.widgets:
        view.add_widget("<system>_virtual_keyboard", Virtual_keyboard, \
            (App.SCREEN_SIZE[0] * 0.5, App.SCREEN_SIZE[1]), anchor=(0, 1))

    view.widgets["<system>_virtual_keyboard"].show()


def close_keyboard():
    from lemapi.constants import App
    from lemapi.widget import Virtual_keyboard

    view = get_view()

    if "virtual_keyboard" not in view.widgets:
        view.add_widget("virtual_keyboard", Virtual_keyboard, \
            (App.SCREEN_SIZE[0] * 0.5, App.SCREEN_SIZE[1]), anchor=(0, 1))

    view.widgets["<system>_virtual_keyboard"].hide()


def get_save_path(app_id=None):
    from lemapi.util import getusername

    if app_id == 0:
        name = "lemapi_desktop"
    elif app_id == None and Instance.app:
        name = Instance.app.get_name()
    elif app_id <= len(Application.apps) and app_id > 0:
        name = Application.apps[app_id - 1].get_name()

    path = os.path.join("/home", getusername(), "saves", name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_default_settings():
    from lemapi.constants import App

    return copy.deepcopy(App.DEFAULT_SETTINGS)


def get_settings():
    if Instance.settings:
        return Instance.settings
    return get_default_settings()
