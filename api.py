# -*- coding: utf-8 -*-

from constants import Instance

def set_activity(activity):
    from activity import Activity, Desktop_activity
    from event_manager import Listener_manager

    if isinstance(activity, Activity):
        if Instance.activity:
            if isinstance(Instance.activity, Desktop_activity):
                print("[INFO] [set_activity] Saving Desktop activity")
                Instance.backup_activity = Instance.activity
            else:
                print("[INFO] [set_activity] Destroying %s" % Instance.activity)
                Instance.activity.destroy()

        Instance.activity = activity
    else:
        print("[WARNING] [set_activity] %s is not an activity." % activity \
            + "Activity instance")


def destroy_activity():
    from activity import Desktop_activity
    from view import Desktop_view

    Instance.activity.destroy()
    if Instance.backup_activity:
        Instance.activity = Instance.backup_activity
    else:
        view = Desktop_view()
        Instance.activity = Desktop_activity(view)


def get_gui():
    from gui import GUI

    if not Instance.gui:
        Instance.gui = GUI()
    return Instance.gui


def get_listener_manager():
    from event_manager import Listener_manager

    if not Instance.listener_manager:
        Instance.listener_manager = Listener_manager()
    return Instance.listener_manager


def restart_app(app_id):
    from application import Application

    for app in Application.apps:
        if app.id == app_id:
            app.reload()
            return True
    print("[WARNING] [restart_app] No app with id=%s" % app_id)
    return False


def force_view_update():
    Instance.activity.view.update()
    Instance.gui.update()
