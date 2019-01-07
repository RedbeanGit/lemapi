# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 19/08/2018
	@version: 1.1
=========================
"""

import os

from game.config import GUI_IMAGE_PATH
from gui.button import Button
from gui.clickable_text import Clickable_text

class Switch_button(Button):

	DEFAULT_KWARGS = {
		"backgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_activated.png"),
		"onHoverBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_activated_hover.png"),
		"onClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_activated_click.png"),
		"onMiddleClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_activated_middle_click.png"),
		"onRightClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_activated_right_click.png"),
		"disableBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_activated_disable.png"),

		"desactivatedBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_desactivated.png"),
		"desactivatedOnHoverBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_desactivated_hover.png"),
		"desactivatedOnClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_desactivated_click.png"),
		"desactivatedOnMiddleClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_desactivated_middle_click.png"),
		"desactivatedOnRightClickBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_desactivated_right_click.png"),
		"desactivatedDisableBackgroundImage": os.path.join(GUI_IMAGE_PATH, "switch button", "switch_desactivated_disable.png")
	}

	def __init__(self, activity, pos, **kwargs):
		Switch_button.updateDefaultKwargs(kwargs)

		self.desactivatedBackgroundImage = None
		self.desactivatedOnHoverBackgroundImage = None
		self.desactivatedOnClickBackgroundImage = None
		self.desactivatedOnMiddleClickBackgroundImage = None
		self.desactivatedOnRightClickBackgroundImage = None
		self.desactivatedDisableBackground = None

		self.activated = True

		Button.__init__(self, activity, pos, **kwargs)

	def loadBackgroundImages(self):
		if self.kwargs["desactivatedBackgroundImage"]:
			self.desactivatedBackgroundImage = self.activity.window.getImage(self.kwargs["desactivatedbackgroundImage"])
		if self.kwargs["desactivatedOnHoverBackgroundImage"]:
			self.desactivatedOnHoverBackgroundImage = self.activity.window.getImage(self.kwargs["desactivatedonHoverBackgroundImage"])
		if self.kwargs["desactivatedOnClickBackgroundImage"]:
			self.desactivatedOnClickBackgroundImage = self.activity.window.getImage(self.kwargs["desactivatedonClickBackgroundImage"])
		if self.kwargs["desactivatedOnMiddleClickBackgroundImage"]:
			self.desactivatedOnMiddleClickBackgroundImage = self.activity.window.getImage(self.kwargs["desactivatedonMiddleClickBackgroundImage"])
		if self.kwargs["desactivatedOnRightClickBackgroundImage"]:
			self.desactivatedOnRightClickBackgroundImage = self.activity.window.getImage(self.kwargs["desactivatedonRightClickBackgroundImage"])
		if self.kwargs["desactivatedDisableBackgroundImage"]:
			self.desactivatedDisableBackgroundImage = self.activity.window.getImage(self.kwargs["desactivateddisableBackgroundImage"])
		Button.loadBackgroundImages(self)

	def update(self, deltaTime):
		if self.activated:
			Button.update(self, deltaTime)
		else:
			if not self.kwargs["enable"] and self.desactivatedDisableBackgroundImage:
				self.activity.window.drawImage(self.desactivatedDisableBackgroundImage, self.getBackgroundPos())
			if self.clicked and self.desactivatedOnClickBackgroundImage:
				self.activity.window.drawImage(self.desactivatedOnClickBackgroundImage, self.getBackgroundPos())
			elif self.rightClicked and self.desactivatedOnRightClickBackgroundImage:
				self.activity.window.drawImage(self.desactivatedOnRightClickBackgroundImage, self.getBackgroundPos())
			elif self.middleClicked and self.desactivatedOnMiddleClickBackgroundImage:
				self.activity.window.drawImage(self.desactivatedOnMiddleClickBackgroundImage, self.getBackgroundPos())
			elif self.hovered and self.desactivatedOnHoverBackgroundImage:
				self.activity.window.drawImage(self.desactivatedOnHoverBackgroundImage, self.getBackgroundPos())
			elif self.desactivatedBackgroundImage:
				self.activity.window.drawImage(self.desactivatedBackgroundImage, self.getBackgroundPos())
			size = self.kwargs["size"]
			Clickable_text.update(self, deltaTime)
			self.kwargs["size"] = size

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