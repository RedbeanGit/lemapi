# -*- coding: utf-8 -*-

from lemapi.api import stop_all_activities
from lemapi.constants import Path
from lemapi.util import read_json, getusername, load_module, reload_module

__author__ = "Julien Dubois"
__version__ = "0.1.0"

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
		self.app_module = None

		print("[lemapi] [INFO] [Application.__init__] New app created " \
			+ "(path=%s, id=%s, name=%s, version=%s)" % (self.path, self.id, \
			self.get_name(), self.get_version()))

	def load_infos(self):
		infos = read_json(os.path.join(self.path, "manifest.json"))
		if infos:
			return infos
		return {}

	def load(self):
		if "main_file" in self.infos:
			print("[lemapi] [INFO] [Application.load] Loading app '%s'" % \
				self.get_name())

			script = self.infos["main_file"]
			try:
				self.app_module = load_module(os.path.join(self.path, script))
			except Exception:
				print("[lemapi] [WARNING] [Application.load] Unable to import " \
					+ "main module of '%s'" % self.get_name())
				traceback.print_exc()

	def reload(self):
		if self.app_module:
			reload_module(self.app_module)
		else:
			print("[lemapi] [WARNING] [Application.reload] App '%s'" % \
				self.get_name() + " not loaded yet!")

	def has_function(self, fct):
		if fct in dir(self.app_module):
			self.buffer = None
			exec("self.buffer = callable(self.app_module.main)")
			c = self.buffer
			del self.buffer
			return c
		return False

	def get_name(self):
		return self.infos.get("name", "unknownApp")

	def get_icon_path(self):
		return os.path.join(self.path, self.infos.get("icon_path", "."))

	def get_version(self):
		return self.infos.get("version", "0.0.0")

	def get_splash_path(self):
		return os.path.join(self.path, self.infos.get("splash_image", "unknownImage.png"))

	def get_desc_image_path(self):
		return os.path.join(self.path, self.infos.get("desc_image", "unknownImage.png"))

	def get_description(self):
		return self.infos.get("description", "")

	def run(self):
		if self.has_function("main"):
			try:
				self.app_module.main(self.id)
			except Exception:
				print("[lemapi] [WARNING] [Application.run] Something wrong " \
					"happened on call of main function (app=%s)" % \
					self.get_name())
				traceback.print_exc()
				self.exit()

	def exit(self):
		if self.has_function("exit"):
			try:
				self.app_module.exit()
			except Exception as e:
				print("[lemapi] [WARNING] [Application.exit] Something wrong " \
					"happened on call of exit function (app=%s error=%s)" % ( \
					self.get_name(), e))
				traceback.print_exc()
		self.kill()

	def kill(self):
		stop_all_activities()

	@staticmethod
	def get_local_apps():
		path = Path.GAMES.format(user=getusername())

		if not os.path.exists(path):
			os.makedirs(path)

		games = os.listdir(path)
		return [os.path.join(path, g) for g in games if "manifest.json" in \
			os.listdir(os.path.join(path, g)) and g not in ("lemapi", \
			"lemapi_desktop")]
