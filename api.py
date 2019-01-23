# -*- coding: utf-8 -*-

from system_instance import Instance

def start_activity(activity):
    print("[INFO] [start_activity] Sleeping %s" % Instance.activities[-1])
    Instance.activities[-1].sleep()
    Instance.activities.append(activity)


def stop_activity():
    import traceback

    if len(Instance.activities) > 1:
        print("[INFO] [stop_activity] Destroying activity %s" % \
            Instance.activities[-1])
        try:
            Instance.activities.pop().destroy()
            Instance.activities[-1].wakeup()
        except Exception:
            print("[WARNING] [stop_activity] Something wrong happened while " \
                + "stopping an activity")
            traceback.print_exc()
    else:
        print("[WARNING] [stop_activity] Unable to destroy Desktop_activity " \
            + "(main activity)")


def stop_all_activities():
    import traceback

    while len(Instance.activities) > 1:
        print("[INFO] [stop_activity] Destroying activity %s" % \
            Instance.activities[-1])
        try:
            Instance.activities.pop().destroy()
        except Exception:
            print("[WARNING] [stop_all_activities] Something wrong happened " \
                "while stopping an activity")
            traceback.print_exc()
    Instance.activities[0].wakeup()


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


def get_activity():
    return Instance.activities[-1]


def get_view():
    return Instance.activities[-1].view


def restart_app():
    if Instance.app:
        Instance.app.reload()
    else:
        print("[WARNING] [restart_app] No app currently running")


def stop_app():
    if Instance.app:
        Instance.app.exit()
        Instance.app = None
    else:
        print("[WARNING] [stop_app] No app currently running")


def get_app_id():
    if Instance.app:
        return Instance.app.id
    return 0


def force_view_update():
    Instance.activities[-1].view.update()
    Instance.gui.update()
