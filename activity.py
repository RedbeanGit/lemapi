# -*- coding: utf-8 -*-

from application import Application
from constants import Instance, Path
from launcher_widget import App_widget, Notif_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from os.path import join
import collection


class Activity(object):
    def __init__(self, view):
        self.view = view

    def update(self, deltatime):
        self.view.update()

    def destroy(self):
        if Instance.activity == self:
            Instance.activity = None


class Desktop_activity(Activity):
    def __init__(self, desktop_view):
        self.apps = []
        super().__init__(desktop_view)

    def load_apps(self):
        apps = Application.get_all_apps()
        for app_name in apps:
            app = Application(join(Path.GAMES, app_name))
            app.load_infos()
            self.apps.append(app)

    def load_icons(self):
        for app in self.apps:
            self.view.add_widget("%s_app_icon" % app.id, App_icon, (0, 0), app)

    def add_notif(self, title, msg):
        self.view.add_widget("notif", Notif_widget, (0, 0), title, msg)
