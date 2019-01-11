# -*- coding: utf-8 -*-

"""
Provide useful classes to create high level graphical components: Widgets.
These classes have been adpated from the Pyoro project.

Created on 28/03/2018
"""

from constants import Path
from util import resizeImage, stretchImage

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os
import pygame.freetype

from os.path import join
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class Widget:

	DEFAULT_KWARGS = {
		"size": [1, 1],
		"anchor": (-1, -1)
	}

	def __init__(self, gui, pos, **kwargs):
		Widget.updateDefaultKwargs(kwargs)
		self.gui = gui
		self.pos = pos
		self.isDestroyed = False
		self.kwargs = dict(kwargs)

	@classmethod
	def updateDefaultKwargs(cls, kwargs):
		for key, value in cls.DEFAULT_KWARGS.items():
			if key not in kwargs:
				kwargs[key] = value

	def update(self):
		pass

	def onEvent(self, event):
		pass

	def config(self, **kwargs):
		for key, value in kwargs.items():
			self.kwargs[key] = value

	def getRealPos(self):
		x, y = self.pos
		w, h = self.kwargs["size"]
		ax, ay = self.kwargs["anchor"]

		return (int(x - w * (ax + 1) / 2), int(y - h * (ay + 1) / 2))

	def isInWidget(self, pos):
		px, py = pos
		x, y = self.getRealPos()
		w, h = self.kwargs["size"]

		return px >= x and px <= x + w and py >= y and py <= y + y

	def destroy(self):
		self.isDestroyed = True


class Text(Widget):

	DEFAULT_KWARGS = {
		"fontSize": 20,
		"font": join(Path.GUI, "font.ttf"),

		"bold": False,
		"wide": False,
		"italic": False,
		"underline": False,
		"verticalMode": False,

		"textColor": (255, 255, 255, 255),
		"backgroundColor": None
	}

	def __init__(self, gui, pos, text, **kwargs):
		Text.updateDefaultKwargs(kwargs)
		Widget.__init__(self, gui, pos, **kwargs)
		self.text = text
		self.createFont()

	def createFont(self):
		self.font = pygame.freetype.Font(self.kwargs["font"])
		kwargs = dict(self.kwargs)
		kwargs.pop("font")
		self.config(**kwargs)

	def update(self):
		surface, rect = self.font.render(self.text, bgcolor=self.kwargs["backgroundColor"])
		self.kwargs["size"] = (rect.width, rect.height)
		self.gui.draw_image(surface, self.getRealPos())
		Widget.update(self)

	def config(self, **kwargs):
		Widget.config(self, **kwargs)
		if "font" in  kwargs:
			self.createFont()
		else:
			if "fontSize" in kwargs:
				self.font.size = kwargs["fontSize"]
			if "bold" in kwargs:
				self.font.strong = kwargs["bold"]
			if "wide" in kwargs:
				self.font.wide = kwargs["wide"]
			if "italic" in kwargs:
				self.font.oblique = kwargs["italic"]
			if "underline" in kwargs:
				self.font.underline = kwargs["underline"]
			if "verticalMode" in kwargs:
				self.font.vertical = kwargs["verticalMode"]
			if "textColor" in kwargs:
				self.font.fgcolor = kwargs["textColor"]


class Eventable_widget(Widget):

	DEFAULT_KWARGS = {
		"enable": True,

		"onClickFct": None,
		"onClickArgs": (),
		"onClickKwargs": {},

		"onHoverFct": None,
		"onHoverArgs": (),
		"onHoverKwargs": {},

		"onMiddleClickFct": None,
		"onMiddleClickArgs": (),
		"onMiddleClickKwargs": {},

		"onRightClickFct": None,
		"onRightClickArgs": (),
		"onRightClickKwargs": {},

		"onWheelFct": None,
		"onWheelArgs": (),
		"onWheelKwargs": {}
	}

	def __init__(self, gui, pos, **kwargs):
		Eventable_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, gui, pos, **kwargs)

		self.hovered = False
		self.clicked = False
		self.middleClicked = False
		self.rightClicked = False

	def onEvent(self, event):
		if self.kwargs["enable"]:
			if event.type == MOUSEMOTION:
				if not self.isInUneventableZone(event.pos):
					if self.isInWidget(event.pos):  self.onHover()
					else:	self.onEndHover()

			elif event.type == MOUSEBUTTONDOWN:
				if not self.isInUneventableZone(event.pos):
					if self.isInWidget(event.pos):
						if event.button == 1:   self.onClick()
						elif event.button == 2: self.onMiddleClick()
						elif event.button == 3: self.onRightClick()
						elif event.button == 4: self.onMouseWheel(1)
						elif event.button == 5: self.onMouseWheel(-1)
					else:
						if event.button == 1:   self.onClickOut()
						elif event.button == 2: self.onMiddleClickOut()
						elif event.button == 3: self.onRightClickOut()
						elif event.button == 4: self.onMouseWheelOut(1)
						elif event.button == 5: self.onMouseWheelOut(-1)

			elif event.type == MOUSEBUTTONUP:
				if not self.isInUneventableZone(event.pos):
					if self.isInWidget(event.pos):
						if event.button == 1:   self.onEndClick()
						elif event.button == 2: self.onEndMiddleClick()
						elif event.button == 3: self.onEndRightClick()
						elif event.button == 4: self.onEndMouseWheel(1)
						elif event.button == 5: self.onEndMouseWheel(-1)
					else:
						if event.button == 1:   self.onEndClickOut()
						elif event.button == 2: self.onEndMiddleClickOut()
						elif event.button == 3: self.onEndRightClickOut()
						elif event.button == 4: self.onEndMouseWheelOut(1)
						elif event.button == 5: self.onEndMouseWheelOut(-1)

	def onHover(self):
		self.hovered = True
		if self.kwargs["onHoverFct"]:
			self.kwargs["onHoverFct"](*self.kwargs["onHoverArgs"], **self.kwargs["onHoverKwargs"])

	def onEndHover(self):
		self.hovered = False

	def onClick(self):
		self.clicked = True

	def onMiddleClick(self):
		self.middleClicked = True

	def onRightClick(self):
		self.rightClicked = True

	def onMouseWheel(self, direction):
		if self.kwargs["onWheelFct"]:
			self.kwargs["onWheelFct"](direction, *self.kwargs["onWheelArgs"], **self.kwargs["onWheelKwargs"])

	def onClickOut(self):
		pass

	def onMiddleClickOut(self):
		pass

	def onRightClickOut(self):
		pass

	def onMouseWheelOut(self, direction):
		pass

	def onEndClick(self):
		if self.clicked:
			self.clicked = False
			if self.kwargs["onClickFct"]:
				self.kwargs["onClickFct"](*self.kwargs["onClickArgs"], **self.kwargs["onClickKwargs"])

	def onEndMiddleClick(self):
		if self.middleClicked:
			self.middleClicked = False
			if self.kwargs["onMiddleClickFct"]:
				self.kwargs["onMiddleClickFct"](*self.kwargs["onMiddleClickArgs"], **self.kwargs["onMiddleClickKwargs"])

	def onEndRightClick(self):
		if self.rightClicked:
			self.rightClicked = False
			if self.kwargs["onRightClickFct"]:
				self.kwargs["onRightClickFct"](*self.kwargs["onRightClickArgs"], **self.kwargs["onRightClickKwargs"])

	def onEndMouseWheel(self, direction):
		pass

	def onEndClickOut(self):
		if self.clicked:
			self.clicked = False

	def onEndMiddleClickOut(self):
		if self.middleClicked:
			self.middleClicked = False

	def onEndRightClickOut(self):
		if self.rightClicked:
			self.rightClicked = False

	def onEndMouseWheelOut(self, direction):
		pass


class Button(Eventable_widget):
	"""
	A simple button widget.
	"""

	DEFAULT_KWARGS = {
		"text": "",
		"textKwargs": {
			"anchor": (0, 0)
		},
		"textAnchor": (0, 0),
		"backgroundImage": join(Path.GUI, "button", "button.png"),
		"onHoverBackgroundImage": join(Path.GUI, "button", \
			"button_hover.png"),
		"onClickBackgroundImage": join(Path.GUI, "button", \
			"button_click.png"),
		"onMiddleClickBackgroundImage": join(Path.GUI, "button", \
			"button_middle_click.png"),
		"onRightClickBackgroundImage": join(Path.GUI, "button", \
			"button_right_click.png"),
		"disableBackgroundImage": join(Path.GUI, "button", \
			"button_disable.png")
	}

	def __init__(self, gui, pos, **kwargs):
		"""
		Initialize a new Button object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of the button in a (x, y) tuple where
			x and y are integers.
		"""

		Button.updateDefaultKwargs(kwargs)
		Button.updateDefaultTextKwargs(kwargs)
		Eventable_widget.__init__(self, gui, pos, **kwargs)
		self.backgroundImages = {}
		self.text = Text(self.gui, self.getTextPos(), self.kwargs["text"], \
			**self.kwargs["textKwargs"])
		self.loadBackgroundImages()

	@classmethod
	def updateDefaultTextKwargs(cls, kwargs):
		for key, value in cls.DEFAULT_KWARGS["textKwargs"].items():
			if key not in kwargs["textKwargs"]:
				kwargs["textKwargs"][key] = value

	def loadBackgroundImages(self):
		"""
		Load the button background images.
		"""

		eventNames = (
			"",
			"onHover",
			"onClick",
			"onMiddleClick",
			"onRightClick",
			"disable"
		)

		for eventName in eventNames:
			if eventName:
				backgroundName = eventName + "BackgroundImage"
			else:
				backgroundName = "backgroundImage"
			self.backgroundImages[eventName] = resizeImage(
				self.gui.get_image(self.kwargs[backgroundName]), \
				self.kwargs["size"])

	def update(self):
		"""
		Redraw the button with the best background for the current event.
		"""

		eventName = ""
		if (not self.kwargs["enable"]):
			eventName = "disable"
		elif self.clicked:
			eventName = "onClick"
		elif self.rightClicked:
			eventName = "onRightClick"
		elif self.middleClicked:
			eventName = "onMiddleClick"
		elif self.hovered:
			eventName = "onHover"

		if eventName in self.backgroundImages:
			self.gui.draw_image(self.backgroundImages[eventName], \
				self.getRealPos())

		self.text.update()
		Eventable_widget.update(self)

	def config(self, **kwargs):
		"""
		Change some attributes of this button and update it.
		"""

		Eventable_widget.config(self, **kwargs)
		if "text" in kwargs:
			self.text.text = kwargs["text"]
		if "textAnchor" in kwargs:
			self.text.pos = self.getTextPos()
		if "textKwargs" in kwargs:
			self.text.config(**kwargs["textKwargs"])

		# If any background is modified
		if "backgroundImage" in kwargs \
		or "onHoverBackgroundImage" in kwargs \
		or "onClickBackgroundImage" in kwargs \
		or "onMiddleClickBackgroundImage" in kwargs \
		or "onRightClickBackgroundImage" in kwargs \
		or "disableBackgroundImage" in kwargs:
			self.loadBackgroundImages()

	def getTextPos(self):
		x, y = self.getRealPos()
		w, h = self.kwargs["size"]
		ax, ay = self.kwargs["textAnchor"]
		return (x + w * (ax + 1) / 2, y + h * (ay + 1) / 2)


class Clickable_text(Text, Eventable_widget):
	""" Clickable text widget """

	DEFAULT_KWARGS = {
		"onClickTextColor": (200, 200, 200, 255),
		"onMiddleClickTextColor": (100, 100, 100, 255),
		"onRightClickTextColor": (220, 220, 220, 255),
		"onHoverTextColor": (230, 230, 230, 255),
		"disableTextColor": (240, 240, 240, 235)
	}

	def __init__(self, gui, pos, text, **kwargs):
		Clickable_text.updateDefaultKwargs(kwargs)
		Text.__init__(self, gui, pos, text, **kwargs)
		Eventable_widget.__init__(self, gui, pos, **self.kwargs)

	def update(self):
		if not self.kwargs["enable"]:
			self.font.fgcolor = self.kwargs["disableTextColor"]
		elif self.clicked:
			self.font.fgcolor = self.kwargs["onClickTextColor"]
		elif self.rightClicked:
			self.font.fgcolor = self.kwargs["onRightClickTextColor"]
		elif self.middleClicked:
			self.font.fgcolor = self.kwargs["onMiddleClickTextColor"]
		elif self.hovered:
			self.font.fgcolor = self.kwargs["onHoverTextColor"]
		else:
			self.font.fgcolor = self.kwargs["textColor"]
		Text.update(self)


class Image_widget(Widget):

	DEFAULT_KWARGS = {
		"size": (0, 0)
	}

	def __init__(self, gui, pos, imagePath, **kwargs):
		"""
		Initialize a new Image_widget object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The position of the widget in a (x, y) tuple, where x and y
			are integers.
		"""

		Image_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, gui, pos, **kwargs)
		tmp_size = self.kwargs["size"]
		self.loadImage(imagePath)

		if tmp_size != (0, 0):
			self.resize(tmp_size)

	def loadImage(self, imagePath):
		"""
		Load an image file to this object.

		:type imagePath: str
		:param imagePath: The filepath to the image to load.
		"""

		self.image = self.gui.get_image(imagePath)
		self.kwargs["size"] = self.image.get_size()

	def update(self):
		"""
		Redraw the image on the game window.
		This method should be called each frame.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds)
		"""
		self.gui.draw_image(self.image, self.getRealPos())
		Widget.update(self)

	def resize(self, newSize):
		"""
		Resize the widget by stretching the image.

		:type newSize: tuple
		:param newSize: The size to give to the widget in a (width, height)
			tuple, where width and height are integers.
		"""

		self.image = resizeImage(self.image, newSize)
		self.kwargs["size"] = tuple(newSize)

	def config(self, **kwargs):
		Widget.config(self, **kwargs)
		if "size" in kwargs:
			self.resize(kwargs["size"])


class Menu_widget(Widget):

	DEFAULT_KWARGS = {
		"backgroundImage": join(Path.GUI, "frame.png")
	}

	def __init__(self, gui, pos, **kwargs):
		Menu_widget.updateDefaultKwargs(kwargs)
		Widget.__init__(self, gui, pos, **kwargs)

		self.subWidgets = {}
		self.backgroundImage = None
		self.loadBackgroundImage()
		self.initWidgets()

	def loadBackgroundImage(self):
		if self.kwargs["backgroundImage"]:
			self.backgroundImage = stretchImage(self.gui.get_image(
				self.kwargs["backgroundImage"]), self.kwargs["size"], 5)

	def initWidgets(self):
		pass

	def addSubWidget(self, widgetName, widgetType, pos, *widgetArgs, **widgetKwargs):
		if widgetName in self.subWidgets:
			print("[WARNING] [Menu_widget.addSubWidget] A widget called " \
				+ "'%s' already exists in this Menu_widget !" % widgetName \
				+ " Destroying it")
			if not self.widgetName[widgetName].isDestroyed:
				self.subWidgets[widgetName].destroy()
		realPos = self.getRealPos()
		self.subWidgets[widgetName] = widgetType(self.gui, \
			(pos[0] + realPos[0], pos[1] + realPos[1]), *widgetArgs, \
			**widgetKwargs)

	def removeSubWidget(self, widgetName):
		if widgetName in self.subWidgets:
			if not self.subWidgets[widgetName].isDestroyed:
				self.subWidgets[widgetName].destroy()
			self.subWidgets.pop(widgetName)
		else:
			print("[WARNING] [Menu_widget.removeSubWidget] No widget called " \
				+ "'%s' in this Menu_widget" % widgetName)

	def configSubWidget(self, widgetName, **kwargs):
		if widgetName in self.subWidgets:
			self.subWidgets[widgetName].config(**kwargs)
		else:
			print("[WARNING] [Menu_widget.configSubWidget] No widget called " \
				+ "'%s' in this Menu_widget" % widgetName)

	def update(self):
		if self.backgroundImage:
			self.gui.draw_image(self.backgroundImage, self.getRealPos())
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.update()

	def onEvent(self, event):
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.onEvent(event)

	def destroy(self):
		for widget in tuple(self.subWidgets.values()):
			if not widget.isDestroyed:
				widget.destroy()
		self.subWidgets.clear()
		Widget.destroy(self)

	def config(self, **kwargs):
		Widget.config(self, **kwargs)
		if "enable" in kwargs:
			for widget in self.subWidgets.values():
				widget.config(enable = kwargs["enable"])


class Setting_bar(Eventable_widget):

	DEFAULT_KWARGS = {
		"lineThickness": 16,
		"cursorWidth": 16,

		"lineImageBorderSize": 4,
		"cursorImageBorderSize": 4,

		"value": 0,

		"lineImage": join(Path.GUI, "setting bar", "line.png"),
		"onHoverLineImage": join(Path.GUI, "setting bar", "line_hover.png"),
		"onClickLineImage": join(Path.GUI, "setting bar", "line_click.png"),
		"onMiddleClickLineImage": join(Path.GUI, "setting bar", "line_middle_click.png"),
		"onRightClickLineImage": join(Path.GUI, "setting bar", "line_right_click.png"),
		"disableLineImage": join(Path.GUI, "setting bar", "line_disable.png"),

		"cursorImage": join(Path.GUI, "setting bar", "cursor.png"),
		"onHoverCursorImage": join(Path.GUI, "setting bar", "cursor_hover.png"),
		"onClickCursorImage": join(Path.GUI, "setting bar", "cursor_click.png"),
		"onMiddleClickCursorImage": join(Path.GUI, "setting bar", "cursor_middle_click.png"),
		"onRightClickCursorImage": join(Path.GUI, "setting bar", "cursor_right_click.png"),
		"disableCursorImage": join(Path.GUI, "setting bar", "cursor_disable.png")
	}

	def __init__(self, gui, pos, **kwargs):
		Setting_bar.updateDefaultKwargs(kwargs)
		Eventable_widget.__init__(self, gui, pos, **kwargs)

		self.lineImage = None
		self.onHoverLineImage = None
		self.onClickLineImage = None
		self.onMiddleClickLineImage = None
		self.onRightClickLineImage = None
		self.disableLineImage = None

		self.cursorImage = None
		self.onHoverCursorImage = None
		self.onClickCursorImage = None
		self.onMiddleClickCursorImage = None
		self.onRightClickCursorImage = None
		self.disableCursorImage = None

		self.cursorPos = self.getCursorPosWithValue(self.kwargs["value"])

		self.loadLineImages()
		self.loadCursorImages()

	def loadLineImages(self):
		imageNames = ("lineImage", "onHoverLineImage", "onClickLineImage", \
			"onMiddleClickLineImage", "onRightClickLineImage", \
			"disableLineImage")

		for imageName in imageNames:
			if self.kwargs[imageName]:
				image = stretchImage( \
					self.gui.get_image(self.kwargs[imageName]), \
					(self.kwargs["size"][0], self.kwargs["lineThickness"]), \
					self.kwargs["lineImageBorderSize"])

				self.__setattr__(imageName, image)

	def loadCursorImages(self):
		imageNames = ("cursorImage", "onHoverCursorImage", "onClickCursorImage", \
			"onMiddleClickCursorImage", "onRightClickCursorImage", \
			"disableCursorImage")

		for imageName in imageNames:
			if self.kwargs[imageName]:
				image = stretchImage( \
					self.gui.get_image(self.kwargs[imageName]), \
					(self.kwargs["cursorWidth"], self.kwargs["size"][1]), \
					self.kwargs["cursorImageBorderSize"])
				self.__setattr__(imageName, image)

	def update(self):
		self.drawLine()
		self.drawCursor()
		Eventable_widget.update(self)

	def drawLine(self):
		if not self.kwargs["enable"] and self.disableLineImage:
			self.gui.draw_image(self.disableLineImage, self.getLinePos())
		if self.clicked and self.onClickLineImage:
			self.gui.draw_image(self.onClickLineImage, self.getLinePos())
		elif self.rightClicked and self.onRightClickLineImage:
			self.gui.draw_image(self.onRightClickLineImage, self.getLinePos())
		elif self.middleClicked and self.onMiddleClickLineImage:
			self.gui.draw_image(self.onMiddleClickLineImage, self.getLinePos())
		elif self.hovered and self.onHoverLineImage:
			self.gui.draw_image(self.onHoverLineImage, self.getLinePos())
		elif self.lineImage:
			self.gui.draw_image(self.lineImage, self.getLinePos())

	def drawCursor(self):
		if not self.kwargs["enable"] and self.disableCursorImage:
			self.gui.draw_image(self.disableCursorImage, self.getCursorPos())
		if self.clicked and self.onClickCursorImage:
			self.gui.draw_image(self.onClickCursorImage, self.getCursorPos())
		elif self.rightClicked and self.onRightClickCursorImage:
			self.gui.draw_image(self.onRightClickCursorImage, self.getCursorPos())
		elif self.middleClicked and self.onMiddleClickCursorImage:
			self.gui.draw_image(self.onMiddleClickCursorImage, self.getCursorPos())
		elif self.hovered and self.onHoverCursorImage:
			self.gui.draw_image(self.onHoverCursorImage, self.getCursorPos())
		elif self.cursorImage:
			self.gui.draw_image(self.cursorImage, self.getCursorPos())

	def getLinePos(self):
		x, y = self.getRealPos()
		w, h = self.kwargs["size"]
		return [x, y + h // 2 - self.kwargs["lineThickness"] // 2]

	def getCursorPos(self):
		return [self.cursorPos - self.kwargs["cursorWidth"] // 2, realPos[1]]

	def onEvent(self, event):
		Eventable_widget.onEvent(self, event)
		if self.kwargs["enable"] and self.clicked:
			if event.type == MOUSEMOTION:
				realPos = self.getRealPos()
				if event.pos[0] >= realPos[0] + self.kwargs["cursorWidth"] / 2 \
					and event.pos[0] <= realPos[0] + self.kwargs["size"][0] \
					- self.kwargs["cursorWidth"] / 2:
					self.cursorPos = event.pos[0]
				elif event.pos[0] < realPos[0] + self.kwargs["cursorWidth"] / 2:
					self.cursorPos = realPos[0] + self.kwargs["cursorWidth"] / 2
				else:
					self.cursorPos = realPos[0] + self.kwargs["size"][0] \
					- self.kwargs["cursorWidth"] / 2

	def getValue(self):
		realPos = self.getRealPos()
		if self.kwargs["size"][0] - self.kwargs["cursorWidth"] != 0:
			return (self.cursorPos - realPos[0] - self.kwargs["cursorWidth"] \
				/ 2) / (self.kwargs["size"][0] - self.kwargs["cursorWidth"])
		return 0.5

	def getCursorPosWithValue(self, value):
		return value * (self.kwargs["size"][0] - self.kwargs["cursorWidth"]) \
			+ self.kwargs["cursorWidth"] / 2 + self.getRealPos()[0]

	def config(self, **kwargs):
		Eventable_widget.config(self, **kwargs)

		if "cursorImageBorderSize" in kwargs or \
			"cursorWidth" in kwargs or \
			"cursorImage" in kwargs or \
			"onHoverCursorImage" in kwargs or \
			"onClickCursorImage" in kwargs or \
			"onMiddleClickCursorImage" in kwargs or \
			"onRightClickCursorImage" in kwargs or \
			"disableCursorImage" in kwargs:
			self.loadCursorImages()

		if "lineImageBorderSize" in kwargs or \
			"lineThickness" in kwargs or \
			"lineImage" in kwargs or \
			"onHoverLineImage" in kwargs or \
			"onClickLineImage" in kwargs or \
			"onMiddleClickLineImage" in kwargs or \
			"onRightClickLineImage" in kwargs or \
			"disableLineImage" in kwargs:
			self.loadLineImages()

		if "value" in kwargs:
			self.cursorPos = self.getCursorPosWithValue(kwargs["value"])


class Switch_button(Button):

	fpath = join(Path.GUI, "switch button")
	DEFAULT_KWARGS = {
		"backgroundImage": join(fpath, "switch_activated.png"),
		"onHoverBackgroundImage": join(fpath, "switch_activated_hover.png"),
		"onClickBackgroundImage": join(fpath, "switch_activated_click.png"),
		"onMiddleClickBackgroundImage": join(fpath, "switch_activated_middle_click.png"),
		"onRightClickBackgroundImage": join(fpath, "switch_activated_right_click.png"),
		"disableBackgroundImage": join(fpath, "switch_activated_disable.png"),

		"desactivatedBackgroundImage": join(fpath, "switch_desactivated.png"),
		"desactivatedOnHoverBackgroundImage": join(fpath, "switch_desactivated_hover.png"),
		"desactivatedOnClickBackgroundImage": join(fpath, "switch_desactivated_click.png"),
		"desactivatedOnMiddleClickBackgroundImage": join(fpath, "switch_desactivated_middle_click.png"),
		"desactivatedOnRightClickBackgroundImage": join(fpath, "switch_desactivated_right_click.png"),
		"desactivatedDisableBackgroundImage": join(fpath, "switch_desactivated_disable.png")
	}

	def __init__(self, gui, pos, **kwargs):
		Switch_button.updateDefaultKwargs(kwargs)

		self.desactivatedBackgroundImages = {}
		self.activated = True

		Button.__init__(self, gui, pos, **kwargs)

	def loadBackgroundImages(self):
		eventNames = (
			"",
			"OnHover",
			"OnClick",
			"OnMiddleClick",
			"OnRightClick",
			"Disable"
		)

		for eventName in eventNames:
			backgroundName = eventName + "BackgroundImage"
			self.desactivatedBackgroundImages[eventName] = resizeImage(
				self.gui.get_image(self.kwargs[backgroundName]), \
				self.kwargs["size"])
		Button.loadBackgroundImages(self)

	def update(self):
		if self.activated:
			Button.update(self)
		else:
			eventName = ""
			if (not self.kwargs["enable"]):
				eventName = "Disable"
			elif self.clicked:
				eventName = "OnClick"
			elif self.rightClicked:
				eventName = "OnRightClick"
			elif self.middleClicked:
				eventName = "OnMiddleClick"
			elif self.hovered:
				eventName = "OnHover"

			if eventName in self.desactivatedBackgroundImages:
				self.gui.draw_image(self.desactivatedBackgroundImages[eventName], \
					self.getRealPos())
			Eventable_widget.update(self)

	def onClickEnd(self):
		if self.clicked:
			self.activated = not self.activated
		Button.onClickEnd(self)

	def config(self, **kwargs):
		Button.config(self, **kwargs)
		if "desactivatedBackgroundImage" in kwargs \
		or "desactivatedOnHoverBackgroundImage" in kwargs \
		or "desactivatedOnClickBackgroundImage" in kwargs \
		or "desactivatedOnMiddleClickBackgroundImage" in kwargs \
		or "desactivatedOnRightClickBackgroundImage" in kwargs \
		or "desactivatedDisableBackgroundImage" in kwargs:
			self.loadBackgroundImages()
