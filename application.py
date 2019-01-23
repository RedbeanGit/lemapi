# -*- coding: utf-8 -*-

from api import stop_all_activities
from constants import Path
from util import read_json, getusername, add_modules

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from importlib import reload
from os.path import exists, join, splitext
import os
import sys
import traceback


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
				add_modules(self.path)
				os.chdir(self.path)

				try:
					exec("import %s" % module)
					exec("self.app_module = %s" % module)
				except ImportError:
					print("[WARNING] [Application.start] Unable to import main" \
						+ " module of '%s'" % self.infos.get("name", "unknownApp"))
					traceback.print_exc()

				self.initable = self.is_initable()
				self.exitable = self.is_exitable()

	def has_function(self, fct):
		if fct in dir(self.app_module):
			self.buffer = None
			exec("self.buffer = callable(self.app_module.main)")
			c = self.buffer
			del self.buffer
			return c
		return False

	def reload(self):
		if self.app_module:
			reload(self.app_module)

	def is_initable(self):
		if self.app_module:
			return self.has_function("main")
		return False

	def is_exitable(self):
		if self.app_module:
			return self.has_function("exit")
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
			except Exception:
				print("[WARNING] [Application.run] Something wrong happened on" \
					+ " call of main function (app=%s)" % self.get_name())
				traceback.print_exc()
				self.exit()

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
		stop_all_activities()
		self.reset()

	@staticmethod
	def get_local_apps():
		path = Path.GAMES.format(user=getusername())
		if not exists(path):
			os.makedirs(path)
		games = os.listdir(path)
		return [join(path, g) for g in games if "manifest.json" in \
			os.listdir(join(path, g))]
