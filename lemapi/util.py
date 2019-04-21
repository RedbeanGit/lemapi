# -*- coding:utf-8 -*-

"""
Provide useful functions.

Created on 02/01/2018
"""

from lemapi.api import stop_app, stop_all_activities, stop_audio_player, get_task_manager
from lemapi.constants import App
from lemapi.system_instance import Instance

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import importlib
import json
import os
import pygame
import sys
import gi
import getpass

gi.require_version('Gdk', '3.0')

from gi.repository import Gdk

################################################################################
### Display Size ###############################################################
################################################################################


def get_monitor_size():
	display = Gdk.Display.get_default()
	monitor = display.get_monitor(0)
	return monitor.get_width_mm(), monitor.get_height_mm()


def get_screen_size():
	screen = Gdk.Screen.get_default()
	return screen.get_width(), screen.get_height()


def get_screen_ratio():
	w, h = get_screen_size()
	if h:
		return w / h
	print("[lemapi] [WARNING] [util.getScreenRatio] Height can't be 0")
	return 1


def get_monitor_density():
	wm, hm = get_monitor_size()
	wp, hp = get_screen_size()
	return wp / wm, hp / hm

################################################################################
### Image operations ###########################################################
################################################################################


def resize_image(image, new_size, antialiasing=True):
	new_size = (int(new_size[0]), int(new_size[1]))
	if antialiasing:
		return pygame.transform.smoothscale(image, new_size)
	return pygame.transform.scale(image, new_size)

def invert_image(image, vertical, horizontal):
	return pygame.transform.flip(image, vertical, horizontal)

def stretch_image(image, new_size, border_size):
	new_size = (int(new_size[0]), int(new_size[1]))
	if border_size < new_size[0] / 2 and border_size < new_size[1] / 2:
		if image.get_alpha() == None:
			back = pygame.Surface(new_size).convert()
		else:
			back = pygame.Surface(new_size, pygame.SRCALPHA, 32).convert_alpha()

		side_len = (image.get_size()[0] - border_size * 2, image.get_size()[1] \
			- border_size * 2)
		new_size_len = (new_size[0] - border_size * 2, new_size[1] - border_size * 2)

		back.blit(image.subsurface((0, 0), (border_size, border_size)).copy(), (0, 0))
		back.blit(pygame.transform.scale(image.subsurface((border_size, 0), \
			(side_len[0], border_size)).copy(), (new_size_len[0], border_size)), \
			(border_size, 0))
		back.blit(image.subsurface((side_len[0] + border_size, 0), \
			(border_size, border_size)).copy(), (new_size_len[0] + border_size, 0))
		back.blit(pygame.transform.scale(image.subsurface((0, border_size), \
			(border_size, side_len[1])).copy(), (border_size,  new_size_len[1])), \
			(0, border_size))
		back.blit(pygame.transform.scale(image.subsurface((border_size, border_size), \
			(side_len[0], side_len[1])), (new_size_len[0], new_size_len[1])), \
			(border_size, border_size))
		back.blit(pygame.transform.scale(image.subsurface((side_len[0] \
			+ border_size, border_size), (border_size, side_len[1])).copy(), \
			(border_size, new_size_len[1])), (new_size_len[0] + border_size, \
			border_size))
		back.blit(image.subsurface((0, side_len[1] + border_size), (border_size, \
			border_size)).copy(), (0, new_size_len[1] + border_size))
		back.blit(pygame.transform.scale(image.subsurface((border_size, side_len[1] \
			+ border_size), (side_len[0], border_size)).copy(), (new_size_len[0], \
			border_size)), (border_size, new_size_len[1] + border_size))
		back.blit(image.subsurface((side_len[0] + border_size, side_len[1] + \
			border_size), (border_size, border_size)).copy(), (new_size_len[0] + \
			border_size, new_size_len[1] + border_size))
		return back
	print("[lemapi] [WARNING] [util.stretch_image] border_size must be inferior to the half size" \
		+ " of the surface")
	return image


def rotate_image(image, angle):
	return pygame.transform.rotate(image, angle)


################################################################################
### File operations ############################################################
################################################################################


def read_file(path):
	if os.path.exists(path):
		if os.path.isfile(path):
			try:
				with open(path, "r") as file:
					return file.read()
			except IOError:
				pass
	return None


def write_file(path, content):
	try:
		with open(path, "w") as file:
			file.write(content)
		return True
	except IOError:
		pass
	return False


def read_json(path):
	content = read_file(path)
	if content != None:
		return json.loads(content)
	return False


def write_json(path, content):
	return write_file(path, json.dumps(content, indent="\t"))


################################################################################
### Introspection ##############################################################
################################################################################


def has_function(module, fct):
	if fct in dir(module):
		exec("c = callable(%s.%s)" % (module.__name__, fct))
		return c
	return False


def has_variable(module, v):
	return v in dir(module)


def add_module_path(path):
	if os.path.exists(path):
		sys.path.append(path)
		files = os.listdir(path)

		for file in files:
			nfp = os.path.join(path, file)
			if os.path.isdir(nfp):
				sys.path.append(nfp)


def load_module(path):
	directory, script = os.path.split(path)
	module_name, ext = os.path.splitext(script)
	module = None

	if ext in (".py", ".pyc", ".pyd", ".pyw"):
		add_module_path(directory)

		# Temporarly changing path to import module
		old_path = os.getcwd()
		os.chdir(directory)
		# Importing the module
		module = importlib.import_module(module_name)
		os.chdir(old_path)

	return module


def reload_module(module):
	importlib.reload(module)


################################################################################
### Program useful #############################################################
################################################################################


def exit(errorLevel=0):
	stop_app()
	Instance.activities[0].destroy()
	stop_audio_player()
	get_task_manager().clear()
	print("[lemapi] [INFO] [exit] LemAPI stopped successfully!")
	sys.exit(errorLevel)


def getusername():
	if App.RPI_ENV:
		return "pi"
	return getpass.getuser()


def get_linux_system_info(prop):
	infos = read_file("/etc/os-release")
	infos = infos.split("\n")
	dic = {}

	for info in infos[:-1]:
		key, value = info.split("=")
		dic[key] = value.replace('"', "")

	if prop in dic:
		return dic[prop]


################################################################################
### Decorators #################################################################
################################################################################


def rpi_only(fct):
	def wrapper(*args, **kwargs):
		if App.RPI_ENV:
			return fct(*args, **kwargs)
	return wrapper