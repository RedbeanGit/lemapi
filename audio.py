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
		self.framerate = 44100
		self.sample_width = 1
		self.chunk_size = 1024

		self.pa = pyaudio.PyAudio()
		self.buffer = bytes(self.get_chunk_size())
		self.thread = None
		self.lock = threading.RLock()
		self.active = False

		self.stream = self.pa.open(
				format = self.pa.get_format_from_width(
					self.sample_width),
				rate = self.framerate,
				channels = self.nb_channels,
				output = True
			)

		self.mixers = []
		self.sounds = {}

	def load_sound(self, path):
		snd = Sound(self)
		self.sounds[path] = snd
		if snd.load(path):
			print("[INFO] [Player.load_sound] Sound '%s' loaded" % path)

	def load_music(self, path):
		msc = Music(self)
		self.sounds[path] = msc
		if msc.load(path):
			print("[INFO] [Player.load_music] Sound '%s' loaded" % path)

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
		self.mixers.append(mixer)

	def remove_mixer(self, mixer):
		if mixer in self.mixers:
			self.mixers.remove(mixer)

	def play(self):
		def loop():
			while self.active:
				with self.lock:
					self.update()

		self.active = True
		self.thread = threading.Thread(target=loop)
		self.thread.start()

	def stop(self):
		if self.active and self.thread:
			self.active = False
			self.thread.join()
			for mixer in self.mixers:
				mixer.clear()

	def update(self):
		for mixer in self.mixers:
			mixer.update()
		self.flush()

	def write(self, chunk):
		self.buffer = audioop.add(self.buffer, chunk, self.sample_width)

	def flush(self):
		self.stream.write(self.buffer)
		self.buffer = bytes(self.get_chunk_size())


class Mixer(object):
	def __init__(self, player):
		self.player = player

		self.sounds = []
		self.playing = True

		self.sound_volume = 1
		self.music_volume = 1
		self.speed = 1

	def __contains__(self, obj):
		return obj in self.sounds

	def add_sound(self, sound):
		self.sounds.append(sound)
		sound.volume = self.sound_volume

	def add_music(self, music):
		self.sounds.append(music)
		music.volume = self.music_volume

	def remove_sound(self, sound):
		if sound in self.sounds:
			self.sounds.remove(sound)

	def clear(self):
		for sound in self.sounds:
			sound.reset()
		self.sounds.clear()
		self.playing = False

	def play(self):
		self.playing = True

	def pause(self):
		self.playing = False

	def update(self):
		chunk_size = self.player.get_chunk_size()
		mixed_chunk = bytes(chunk_size)
		if self.playing:
			for sound in self.sounds:
				if sound.loaded and sound.playing:

					if sound.is_ended():
						sound.reset()
						sound.play_count -= 1

					if sound.play_count == 0:
						sound.stop()
					else:
						chunk = sound.get_chunk()

						try:
							mixed_chunk = audioop.add(mixed_chunk, chunk, \
								self.player.sample_width)
						except Exception:
							print("[WARNING] [Mixer.update] Something wrong " \
								"happened when adding 2 audio chunks")
							traceback.print_exc()
							sound.unload()

						mixed_chunk = audioop.ratecv(mixed_chunk, \
							self.player.sample_width, \
							self.player.nb_channels, \
							self.player.framerate, \
							(self.player.framerate // self.speed),
							None)[0]

		self.player.write(mixed_chunk)

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

	def set_pos(self, pos):
		if self.loaded:
			self.pos = pos

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
					print("[WARNING] [Sound.load] Unmanaged header for '%s'" \
						% path)
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
				print("[WARNING] [Music.load] Unmanaged header for '%s'" \
					% path)
			except Exception:
				print('[WARNING] [Music.load] Unable to load "%s"' % self.path)
		else:
			print('[WARNING] [Music.load] Unable to find "%s"' % self.path)
		return False

	def unload(self):
		if self.loaded:
			self.wave_file.close()
		super().unload()

	def set_pos(self, pos):
		if self.loaded:
			self.wave_file.setpos(pos)
		super().set_pos(pos)

	def reset(self):
		if self.loaded:
			self.wave_file.rewind()
		super().reset()

	def is_ended(self):
		if self.loaded:
			return self.pos >= self.wave_file.getnframes()
		return False

	def copy(self, sound):
		if sound.loaded:
			self.load(sound.path)

	def get_chunk(self):
		chunk_size = self.player.get_chunk_size()

		if self.loaded:
			chunk = self.wave_file.readframes(self.player.chunk_size)
			self.pos = self.wave_file.tell()
			return chunk + bytes(chunk_size - len(chunk))

		return bytes(chunk_size)
