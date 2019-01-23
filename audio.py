# -*- coding: utf-8 -*-

"""
Provides some audio classes like Sound, Music, Player and Mixer.

Created on 21/01/2019
"""

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import audioop
import pyaudio
import traceback
import threading
import wave

from os.path import exists, join


class Player(object):
	def __init__(self):
		self.nb_channels = 2
		self.frequency = 44100
		self.sample_width = 1
		self.chunk_size = 1024

		self.pa = pyaudio.PyAudio()
		self.thread = None
		self.active = False

		self.mixers = []
		self.sounds = {}

	def load_sound(self, path):
		if exists(path):
			snd = Sound(self)
			snd.load(path)
			self.sounds[path] = snd
			print("[INFO] [Player.load_sound] Sound '%s' loaded" % path)
		else:
			print("[WARNING] [Player.load_sound] Unable to find '%s'" path)

	def load_music(self, path):
		if exists(path):
			msc = Music(self)
			msc.load(path)
			self.sounds[path] = msc
			print("[INFO] [Player.load_music] Sound '%s' loaded" % path)
		else:
			print("[WARNING] [Player.load_music] Unable to find '%s'" path)

	def get_sound(self, path):
		snd = Sound(self)
		if path in self.sounds:
			snd.copy(self.sounds[path])
		return snd

	def get_music(self, path):
		if path in self.sounds:
			return self.sounds[path]
		return Music(self)

	def get_chunk_size(self):
		return self.chunk_size * self.sample_width * self.nb_channels

	def add_mixer(self, mixer):
		self.mixer.append(mixer)

	def remove_mixer(self, mixer):
		if mixer in self.mixers:
			self.mixers.remove(mixer)

	def play(self):
		def loop(self):
			while self.active:
				self.update()

		self.active = True
		self.thread = threading.Thread(target=loop)
		self.thread.start()

	def stop(self):
		if self.active and self.thread:
			self.active = False
			self.thread.join()

	def update(self):
		for mixer in self.mixers:
			mixer.update()


class Mixer(object):
	def __init__(self, player):
		self.player = player
		self.stream = self.player.pa.open(
				format = self.player.pa.get_format_from_width(
					self.player.samples_width),
				rate = self.player.framerate,
				channels = self.player.nb_channels,
				output = True
			)
		self.sounds = []

		self.sound_volume = 1
		self.music_volume = 1
		self.speed = 1

	def add_sound(self, sound):
		self.sounds.append(sound)
		sound.volume = self.sound_volume

	def add_music(self, music):
		self.sounds.append(music)
		music.volume = self.music_volume

	def remove_sound(self, sound):
		if sound in self.sounds:
			self.sounds.remove(sound)

	def update(self):
		chunk_size = self.player.get_chunk_size()
		mixed_chunk = bytes(chunk_size)
		for sound in self.sounds:
			if sound.loaded and sound.playing:

				if sound.is_ended() and sound.play_count != 0:
					sound.reset()
					sound.play_count -= 1

				chunk = sound.get_chunk()

				try:
					mixed_chunk = audioop.add(mixed_chunk, chunk, self.sample_width)
				except Exception:
					print("[WARNING] [Mixer.update] Something wrong happened " \
						+ "when adding 2 audio chunks")
					traceback.print_exc()
					sound.unload()

		self.stream.write(mixed_chunk)

	def set_speed(self, speed):
		if speed > 0:
			self.speed = speed

	def set_sound_volume(self, volume):
		if volume >= 0 and volume <= 1:
			self.sound_volume = volume

			for sound in self.sounds:
				if not isinstance(sound, Music):
					sound.volume = volume

	def set_music_volume(self, volume):
		if volume >= 0 and volume <= 1:
			self.music_volume = volume

			for sound in self.sounds:
				if isinstance(sound, Music):
					sound.volume = volume


class Sound(object):
	def __init__(self, player):
		self.path = ""
		self.player = player
		self.samples = bytes()
		self.loaded = False
		self.playing = False
		self.pos = 0
		self.volume = 1
		self.play_count = 1

	def play(self):
		self.playing = True

	def pause(self):
		self.playing = False

	def stop(self):
		self.playing = False
		self.play_count = 1
		self.reset()

	def set_play_count(self, count):
		self.play_count = count

	def reset(self):
		self.pos = 0

	def load(self, path):
		if exists(path):
			try:
				with wave.open(path, "rb") as wf:
					if wf.getframerate() == self.player.framerate \
					and wf.getnchannels() == self.player.nb_channels \
					and wf.getsampwidth() == self.player.sample_width:
						self.samples = wf.readframes(wf.getnframes() - 1)
						self.path = path
						self.loaded = True
						return True
			except Exception:
				print('[WARNING] [Sound.load] Unable to load "%s"' % self.path)
		else:
			print('[WARNING] [Sound.load] Unable to find "%s"' % self.path)
		return False

	def unload(self):
		if self.loaded:
			self.samples = bytes()
			self.path = ""
			self.playing = False
			self.loaded = False
			self.pos = 0

	def is_ended(self):
		return self.pos >= len(self.samples) \
			/ self.player.sample_width \
			/ self.player.nb_channels

	def copy(self, sound):
		if sound.loaded:
			self.path = sound.path
			self.samples = sound.samples
			self.loaded = True
		else:
			print("[WARNING] [Sound.copy] Unable to copy an unloaded sound!")

	def get_chunk(self):
		chunk_size = self.player.get_chunk_size()

		if self.loaded:
			sample_pos = self.pos \
				* self.player.nb_channels \
				* self.player.sample_width

			chunk = self.samples[sample_pos:sample_pos+chunk_size]
			self.pos += self.player.chunk_size

			return chunk + bytes(chunk_size - len(sample))

		return bytes(chunk_size)


class Music(Sound):
	def __init__(self, player):
		super().__init__(player)
		self.wave_file = None

	def load(self, path):
		if exists(path):
			if self.loaded:
				self.unload()

			try:
				wf = wave.open(path, "rb")

				if wf.getframerate() == self.player.framerate \
				and wf.getnchannels() == self.player.nb_channels \
				and wf.getsampwidth() == self.player.sample_width:
					self.wave_file = wf
					self.path = path
					self.loaded = True
					return True
				wf.close()
			except Exception:
				print('[WARNING] [Music.load] Unable to load "%s"' % self.path)
		else:
			print('[WARNING] [Music.load] Unable to find "%s"' % self.path)
		return False

	def unload(self):
		if self.loaded:
			self.wave_file.close()
		super().unload()

	def reset(self):
		if self.loaded:
			self.wave_file.rewind()
		super().reset()

	def copy(self, sound):
		if sound.loaded:
			self.load(sound.path)
		else:
			print("[WARNING] [Music.copy] Unable to copy an unloaded sound!")

	def get_chunk(self):
		chunk_size = self.player.get_chunk_size()

		if self.loaded:
			chunk = self.wave_file.readframes(self.player.chunk_size)
			self.pos = self.wave_file.tell()
			return chunk + bytes(chunk_size - len(chunk))

		return bytes(chunk_size)
