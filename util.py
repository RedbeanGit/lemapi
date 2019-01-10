# -*- coding:utf-8 -*-

"""
Provide useful functions.

Created on 02/01/2018
"""

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import json
import os
import pygame
import sys
import gi

gi.require_version('Gdk', '3.0')

from gi.repository import Gdk

################################################################################
### Display Size ###############################################################
################################################################################


def getMonitorSize():
	"""
	Return the screen size in mm.

	:rtype: tuple
	:returns: (width, height) tuple where width and height are ints which
		represent the default screen size in millimeters.
	"""

	display = Gdk.Display.get_default()
	monitor = display.get_monitor(0)
	return monitor.get_width_mm(), monitor.get_height_mm()


def getScreenSize():
	"""
	Return the screen size in pixels.

	:rtype: tuple
	:returns: (width, height) tuple where width and height are ints which
		represent the default screen size in pixels.
	"""

	screen = Gdk.Screen.get_default()
	return screen.get_width(), screen.get_height()


def getScreenRatio():
	"""
	Return the screen resolution (width / height).

	:rtype: float
	:returns: A floating point value representing the ratio width / height.
	"""

	w, h = getScreenSize()
	if h:
		return w / h
	print("[WARNING] [util.getScreenRatio] Height can't be null")
	return 1


def getMonitorDensity():
	wm, hm = getMonitorSize()
	wp, hp = getScreenSize()
	return wp / wm, hp / hm

################################################################################
### Image operations ###########################################################
################################################################################


def resizeImage(image, newSize):
    """
    Resize an image (a pygame surface).
    This function comes from the Pyoro project.

    :type image: pygame.surface.Surface
    :param image: The image to resize.

    :type newSize: tuple
    :param newSize: The new size of the image in a (width, height) tuple where
        width and height are integers.

    :rtype: pygame.surface.Surface
    :returns: A new pygame surface with the given size.
    """

    newSize = (int(newSize[0]), int(newSize[1]))
    return pygame.transform.scale(image, newSize)

def invertImage(image, vertical, horizontal):
    """
    Revert an image (a pygame surface) as if it was looking into a mirror.

    :type image: pygame.surface.Surface
    :param image: The image to revert.

    :type vertical: bool
    :param vertical: If True, the image will be reverted vertically.

    :type horizontal: bool
    :param horizontal: If True, the image will be reverted horizontally.

    :rtype: pygame.surface.Surface
    :returns: A new pygame surface reverted.
    """

    return pygame.transform.flip(image, vertical, horizontal)

def stretchImage(image, newSize, borderSize):
    """
    Resize an image (a pygame surface) but do not deform it. It only resize
    borders and center as 9-path images. Useful for buttons or gui frames.

    :type image: pygame.surface.Surface
    :param image: The image to resize.

    :type newSize: tuple
    :param newSize: The new size to give to the output image.

    :type borderSize: int
    :param borderSize: The width of the borders which can be stretch.

    :rtype: pygame.surface.Surface
    :returns: A new pygame surface with the given size.
    """

    newSize = (int(newSize[0]), int(newSize[1]))
    if borderSize <= newSize[0] / 2 and borderSize <= newSize[1] / 2:
        borderSize = int(borderSize)
    else:
        borderSize = min(newSize) // 2

    if image.get_alpha == None:
        back = pygame.Surface(newSize).convert()
    else:
        back = pygame.Surface(newSize).convert_alpha()

    sideLength = (image.get_size()[0] - borderSize * 2, image.get_size()[1] \
        - borderSize * 2)
    newSideLength = (newSize[0] - borderSize * 2, newSize[1] - borderSize * 2)

    back.blit(image.subsurface((0, 0), (borderSize, borderSize)).copy(), (0, 0))
    back.blit(pygame.transform.scale(image.subsurface((borderSize, 0), \
        (sideLength[0], borderSize)).copy(), (newSideLength[0], borderSize)), \
        (borderSize, 0))
    back.blit(image.subsurface((sideLength[0] + borderSize, 0), \
        (borderSize, borderSize)).copy(), (newSideLength[0] + borderSize, 0))
    back.blit(pygame.transform.scale(image.subsurface((0, borderSize), \
        (borderSize, sideLength[1])).copy(), (borderSize,  newSideLength[1])), \
        (0, borderSize))
    back.blit(pygame.transform.scale(image.subsurface((borderSize, borderSize), \
        (sideLength[0], sideLength[1])), (newSideLength[0], newSideLength[1])), \
        (borderSize, borderSize))
    back.blit(pygame.transform.scale(image.subsurface((sideLength[0] \
        + borderSize, borderSize), (borderSize, sideLength[1])).copy(), \
        (borderSize, newSideLength[1])), (newSideLength[0] + borderSize, \
        borderSize))
    back.blit(image.subsurface((0, sideLength[1] + borderSize), (borderSize, \
        borderSize)).copy(), (0, newSideLength[1] + borderSize))
    back.blit(pygame.transform.scale(image.subsurface((borderSize, sideLength[1] \
        + borderSize), (sideLength[0], borderSize)).copy(), (newSideLength[0], \
        borderSize)), (borderSize, newSideLength[1] + borderSize))
    back.blit(image.subsurface((sideLength[0] + borderSize, sideLength[1] + \
        borderSize), (borderSize, borderSize)).copy(), (newSideLength[0] + \
        borderSize, newSideLength[1] + borderSize))
    return back

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
    return content


def write_json(path, content):
    write_file(path, json.dumps(content, indent="\t"))

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

################################################################################
### Introspection ##############################################################
################################################################################


def exit(errorLevel = 0):
	sys.exit(errorLevel)
