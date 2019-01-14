# -*- coding: utf-8 -*-

from constants import Path
from util import read_json, has_function, getusername

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from os.path import exists, join, splitext
import os
import sys


class Application(object):

    nb_apps = 0

    def __init__(self, path):
        Application.nb_apps += 1
        self.path = path
        self.id = Application.nb_apps
        self.infos = self.load_infos()
        print("[INFO] [Application.__init__] New app created " \
            + "(path=%s, id=%s, infos=%s)" % (self.path, self.id, self.infos))
        self.reset()

    def reset(self):
        self.app_module = None
        self.initable = False
        self.updatable = False
        self.killable = False

    def load_infos(self):
        print(self.path)
        infos = read_json(join(self.path, "manifest.json"))
        if infos:
            return infos
        return {}

    def start(self):
        if "main_file" in self.infos:
            main = self.infos["main_file"]
            module = splitext(main)[0]
            if exists(join(self.path, main)):
                Instance.app = self
                sys.path.append(self.path)

                try:
                    exec("import %s" % module)
                    exec("self.app_module = %s" % module)
                except ImportError:
                    print("[WARNING] [Application.start] Unable to import main" \
                        + " module of '%s'" % self.infos.get("name", "unknownApp"))

                self.initable = self.is_initable()
                self.updatable = self.is_updatable()
                self.killable = self.is_killable()

    def is_initable(self):
        if self.app_module:
            return has_function(self.app_module, "main")
        return False

    def is_updatable(self):
        if self.app_module:
            return has_function(self.app_module, "update")
        return False

    def is_killable(self):
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
            self.app_module.main()

    def update(self, deltatime):
        if self.updatable:
            self.app_module.update(deltatime)

    def kill(self):
        if self.killable:
            self.app_module.kill()
        Instance.app = None
        self.reset()

    @staticmethod
    def get_local_apps():
        path = Path.GAMES.format(user=getusername())
        if not exists(path):
            os.makedirs(path)
        games = os.listdir(path)
        return [join(path, g) for g in games if "manifest.json" in \
            os.listdir(join(path, g))]
