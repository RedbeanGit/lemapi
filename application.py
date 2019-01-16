# -*- coding: utf-8 -*-

from api import destroy_activity
from constants import Path
from util import read_json, has_function, getusername

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from importlib import reload
from os.path import exists, join, splitext
import os
import sys


class Application(object):

    nb_apps = 0
    apps = []

    def __init__(self, path):
        Application.nb_apps += 1
        Application.apps.append(self)

        self.path = path
        self.id = Application.nb_apps
        self.infos = self.load_infos()
        print("[INFO] [Application.__init__] New app created " \
            + "(path=%s, id=%s, name=%s, version=%s)" % (self.path, self.id, \
            self.get_name(), self.get_version()))
        self.reset()

    def reset(self):
        self.app_module = None
        self.initable = False
        self.exitable = False

    def load_infos(self):
        infos = read_json(join(self.path, "manifest.json"))
        if infos:
            return infos
        return {}

    def start(self):
        if "main_file" in self.infos:
            main = self.infos["main_file"]
            module = splitext(main)[0]
            if exists(join(self.path, main)):
                sys.path.append(self.path)

                try:
                    exec("import %s" % module)
                    exec("self.app_module = %s" % module)
                except ImportError:
                    print("[WARNING] [Application.start] Unable to import main" \
                        + " module of '%s'" % self.infos.get("name", "unknownApp"))

                self.initable = self.is_initable()
                self.exitable = self.is_exitable()

    def reload(self):
        if self.app_module:
            reload(self.app_module)

    def is_initable(self):
        if self.app_module:
            return has_function(self.app_module, "main")
        return False

    def is_exitable(self):
        if self.app_module:
            return has_function(self.app_module, "kill")
        return False

    def get_name(self):
        return self.infos.get("name", "unknownApp")

    def get_icon_path(self):
        return join(self.path, self.infos.get("icon_path", "."))

    def get_version(self):
        return self.infos.get("version", "0.0.0")

    def run(self):
        if self.initable:
            try:
                self.app_module.main(self.id)
            except Exception as e:
                print("[WARNING] [Application.run] Something wrong happened on" \
                    + " call of main function (app=%s error=%s)" % ( \
                    self.get_name(), e))
                self.kill()

    def exit(self):
        if self.exitable:
            try:
                self.app_module.exit()
            except Exception as e:
                print("[WARNING] [Application.exit] Something wrong happened" \
                    + " on call of exit function (app=%s error=%s)" % ( \
                    self.get_name(), e))
        self.kill()

    def kill(self):
        destroy_activity()
        self.reset()

    @staticmethod
    def get_local_apps():
        path = Path.GAMES.format(user=getusername())
        if not exists(path):
            os.makedirs(path)
        games = os.listdir(path)
        return [join(path, g) for g in games if "manifest.json" in \
            os.listdir(join(path, g))]
