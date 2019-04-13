# -*- coding: utf-8 -*-

"""
Provides some audio classes like Sound, Music, Player and Mixer.

Created on 21/01/2019
"""

from lemapi.system_instance import Instance

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
		self.framerate = 22050
		self.sample_width = 2
		self.chunk_size = 1024

		self.pa = pyaudio.PyAudio()
		self.buffer = bytes(self.get_chunk_size())
		self.thread = None
		self.lock = threading.RLock()
		self.active = False
		self.speed = 1
		self.volume = 1

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
			print("[lemapi] [INFO] [Player.load_sound] Sound '%s' loaded" % path)

	def load_music(self, path):
		msc = Music(self)
		self.sounds[path] = msc
		if msc.load(path):
			print("[lemapi] [INFO] [Player.load_music] Sound '%s' loaded" % path)

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
		print("[lemapi] [INFO] [Player.play] Audio started !")

	def stop(self):
		if self.active and self.thread:
			self.active = False
			self.thread.join()
			for mixer in self.mixers:
				mixer.clear()
			print("[lemapi] [INFO] [Player.stop] Audio stopped successfully !")

	def update(self):
		for mixer in self.mixers:
			mixer.update()
		self.flush()

	def set_speed(self, speed):
		if speed > 0:
			self.speed = speed

	def set_volume(self, volume):
		if volume >= 0 and volume <= 0:
			self.volume = volume

	def write(self, chunk):
		self.buffer = audioop.add(self.buffer, chunk, self.sample_width)

	def flush(self):
		self.buffer = audioop.ratecv(self.buffer, \
			self.sample_width, \
			self.nb_channels, \
			self.framerate, \
			int(self.framerate / self.speed),
			None)[0]
		self.buffer = audioop.mul(self.buffer, self.sample_width, \
			Instance.settings.get("sound_volume", 1))

		self.stream.write(self.buffer)
		self.buffer = bytes(self.get_chunk_size())


class Mixer(object):
	def __init__(self, player):
		self.player = player
		self.sounds = []
		self.playing = True
		self.volume = 1

	def __contains__(self, obj):
		return obj in self.sounds

	def add_sound(self, sound):
		self.sounds.append(sound)

	def add_music(self, music):
		self.sounds.append(music)

	def remove_sound(self, sound):
		if sound in self.sounds:
			self.sounds.remove(sound)

	def clear(self):
		for sound in self.sounds:
			sound.stop()
		self.sounds.clear()

	def stop_audio(self):
		for sound in self.sounds:
			sound.stop()

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
							mixed_chunk = audioop.add(mixed_chunk, audioop.mul( \
								chunk, self.player.sample_width, sound.volume * \
								self.volume * self.player.volume), self.player.sample_width)
						except Exception:
							print("[lemapi] [WARNING] [Mixer.update] Something " \
								+ "wrong happened when mixing 2 audio chunks")
							traceback.print_exc()
							sound.unload()

		self.player.write(mixed_chunk)

	def set_volume(self, volume):
		if volume >= 0 and volume <= 1:
			self.volume = volume


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
					framerate = wf.getframerate()
					nb_channels = wf.getnchannels()
					sample_width = wf.getsampwidth()

					if framerate == self.player.framerate \
					and nb_channels == self.player.nb_channels \
					and sample_width == self.player.sample_width:
						self.samples = wf.readframes(wf.getnframes() - 1)
						self.path = path
						self.loaded = True
						return True
					print("[lemapi] [WARNING] [Sound.load] Unmanaged header for " \
						+ "%s" % path + " (framerate=%s, channels=%s, " % \
						(framerate, nb_channels) + "sample_width=%s)" % \
						sample_width)
			except Exception:
				print('[lemapi] [WARNING] [Sound.load] Unable to load "%s"' % \
					path)
		else:
			print('[lemapi] [WARNING] [Sound.load] Unable to find "%s"' % path)
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

			return chunk + bytes(chunk_size - len(chunk))

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
				framerate = wf.getframerate()
				nb_channels = wf.getnchannels()
				sample_width = wf.getsampwidth()

				if framerate == self.player.framerate \
				and nb_channels == self.player.nb_channels \
				and sample_width == self.player.sample_width:
					self.wave_file = wf
					self.path = path
					self.loaded = True
					return True
				wf.close()
				print("[lemapi] [WARNING] [Sound.load] Unmanaged header for %s" \
					% path + " (framerate=%s, channels=%s, " % (framerate, \
					nb_channels) + "sample_width=%s)" % sample_width)
			except Exception:
				print('[lemapi] [WARNING] [Music.load] Unable to load "%s"' % \
					path)
		else:
			print('[lemapi] [WARNING] [Music.load] Unable to find "%s"' % path)
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
