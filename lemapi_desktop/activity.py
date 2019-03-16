# -*- coding: utf-8 -*-

from lemapi_desktop.util import load_images, load_sounds, load_musics
from lemapi_desktop.view import Desktop_view
from lemapi_desktop.widget import App_widget, Notif_widget

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import threading

from lemapi.activity import Activity
from lemapi.api import get_audio_player, get_gui, get_global_listener_manager, \
    get_task_manager, get_save_path
from lemapi.application import Application
from lemapi.audio import Mixer
from lemapi.constants import Path, App
from lemapi.event_manager import Event
from lemapi.system_instance import Instance
from lemapi.task_manager import Analog_task_delay, Task_delay
from lemapi.util import getusername, exit, read_json

from os.path import join
from pygame.locals import K_LCTRL, K_ESCAPE


class Splash_activity(Activity):
    def __init__(self, splash_view):
        super().__init__(splash_view)
        self.mixer = None
        self.loaded = False

        self.init_events()
        self.load_splash_images()
        tm = get_task_manager()

        if App.SPLASH_ANIMATION:
            tm.add_task("start_background_rotate", Task_delay(0.8, \
                self.start_background_rotate))
            tm.add_task("start_appear_title", Task_delay(3.8, \
                self.start_appear_title))
        else:
            self.appear_title(1)
            self.appear_loading(1)

        self.init_mixer()
        threading.Thread(target=self.load_resources).start()

    def init_events(self):
        lmgr = get_global_listener_manager()
        event = Event(exit)
        lmgr.km.add_key_down_event(event, K_LCTRL, K_ESCAPE)

    def load_splash_images(self):
        names = ("labyrinth_part_1.png", "labyrinth_part_2.png", \
            "labyrinth_part_3.png", "lem_logo.png")
        gui = get_gui()

        for name in names:
            gui.load_image(join(Path.IMAGES, "splash", name))

        self.view.create_labyrinth()
        self.view.create_logo()

    def init_mixer(self):
        ap = get_audio_player()
        self.mixer = Mixer(ap)
        ap.add_mixer(self.mixer)

    def load_resources(self):
        load_musics()
        self.start_music()
        load_sounds()
        load_images()
        self.loaded = True

    def start_music(self):
        music_path = join(Path.MUSICS, "startup_music.wav")
        music = get_audio_player().get_music(music_path)
        music.play()
        self.mixer.add_music(music)

    def start_background_rotate(self):
        self.view.widgets["labyrinth_widget"].rotate = True

    def start_appear_title(self):
        get_task_manager().add_task("appear_title", Analog_task_delay(1.5, \
            self.appear_title))

    def appear_title(self, value):
        self.view.widgets["title_image"].set_opacity(value * 255)

    def update(self, deltatime):
        if self.loaded:
            self.create_desktop()
        super().update(deltatime)

    def create_desktop(self):
        self.destroy()
        view = Desktop_view()
        Instance.activities[0] = Desktop_activity(view)
        view.init_events()

    def destroy(self):
        tm = get_task_manager()
        tm.remove_task("start_background_rotate")
        tm.remove_task("start_appear_title")
        super().destroy()


class Desktop_activity(Activity):
    def __init__(self, desktop_view):
        super().__init__(desktop_view)
        self.apps = []
        self.load_apps()
        self.load_icons()
        print("[lemapi] [INFO] [Desktop_activity.__init__] Activity started " \
            + "successfully !")

    def load_apps(self):
        apps = Application.get_local_apps()
        path = Path.GAMES.format(user=getusername())
        for app_path in apps:
            app = Application(app_path)
            app.load_infos()
            self.apps.append(app)

    def load_icons(self):
        for app in self.apps:
            wname = "%s_app_widget" % app.id

            self.view.add_widget(wname, App_widget, (0, 0), \
                app, anchor=(0, 0))
            self.view.add_app(wname)
        self.view.reset_angle()

    def add_notif(self, title, msg):
        self.view.add_widget("notif", Notif_widget, (0, 0), title, msg)
