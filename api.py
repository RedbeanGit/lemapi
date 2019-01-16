# -*- coding: utf-8 -*-

from constants import Instance

def set_activity(activity):
    from activity import Activity, Desktop_activity

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
            "Activity instance")


def destroy_activity():
    from activity import Desktop_activity

    destroy_view()
    Instance.activity.destroy()
    if Instance.backup_activity:
        Instance.activity = Instance.backup_activity
    else:
        Instance.activity = Desktop_activity(Instance.view)


def destroy_view():
    from view import Desktop_view

    Instance.view.destroy()
    if Instance.backup_view:
        Instance.view = Instance.backup_view
    else:
        Instance.view = Desktop_view()


def set_view(view):
    from view import View

    if Instance.view:
        print("[INFO] [set_view] Destroying %s" % Instance.view)
        Instance.view.destroy()
    if isinstance(view, View):
        Instance.view = view
    else:
        print("[WARNING] [set_view] %s is not a view." % view \
            "View instance")

def get_gui():
    from gui import GUI
    
    If not Instance.gui:
        Instance.gui = GUI()
    return Instance.gui


def restart_app(app_id):
    from application import Application

    for app in Application.apps:
        if app.id == app_id:
            app.reload()
            return True
    print("[WARNING] [restart_app] No app with id=%s" % app_id)
    return False
