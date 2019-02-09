# -*- coding: utf-8 -*-

from api import get_listener_manager, get_task_manager, get_gui, get_audio_player
from application import Application
from audio import Mixer
from constants import Path
from event_manager import Event
from launcher_widget import App_widget, Notif_widget
from system_instance import Instance
from task_manager import Analog_task_delay, Task_delay
from util import getusername, exit, rotate_image
from view import Desktop_view

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from os.path import join
from pygame.locals import K_LCTRL, K_ESCAPE


class Activity(object):
    def __init__(self, view):
        self.view = view
        self.events = []

    def update(self, deltatime):
        self.view.update()

    def sleep(self):
        for event in self.events:
            event.enable = False

    def wakeup(self):
        for event in self.events:
            event.enable = True

    def destroy(self):
        self.view.destroy()


class Splash_activity(Activity):
    def __init__(self, splash_view):
        super().__init__(splash_view)
        self.mixer = None

        tm = get_task_manager()
        tm.add_task("start_background_rotate", Task_delay(0.8, \
            self.start_background_rotate))
        tm.add_task("start_appear_title", Task_delay(3.8, self.start_appear_title))
        tm.add_task("load_resources", Task_delay(8.5, self.load_resources))

        self.init_mixer()
        print("[lemapi] [INFO] [Splash_activity.__init__] Activity started " \
            + "successfully !")

    def init_mixer(self):
        ap = get_audio_player()
        self.mixer = Mixer(ap)
        ap.add_mixer(self.mixer)

        music_path = join(Path.MUSIC, "startup_music.wav")
        ap.load_music(music_path)
        music = ap.get_music(music_path)
        music.play()
        self.mixer.add_music(music)

    def start_appear_title(self):
        get_task_manager().add_task("appear_title", Analog_task_delay(1.5, \
            self.appear_title))

    def start_appear_loading(self):
        get_task_manager().add_task("appear_loading", Analog_task_delay(1.5, \
            self.appear_loading))

    def start_background_rotate(self):
        self.view.widgets["labyrinth_widget"].rotate = True

    def load_resources(self):
        self.start_appear_loading()
        get_gui().load_images()
        tm = get_task_manager()
        tm.add_task("create_desktop", \
            Task_delay(7, self.create_desktop))

    def appear_title(self, value):
        self.view.widgets["title_image"].set_opacity(value * 255)

    def appear_loading(self, value):
        self.view.widgets["loading_text"].config(textColor=(75, 75, 75, \
            int(value * 255)))

    def create_desktop(self):
        view = Desktop_view()
        Instance.activities[0] = Desktop_activity(view)
        self.destroy()


class Desktop_activity(Activity):
    def __init__(self, desktop_view):
        super().__init__(desktop_view)
        self.apps = []
        self.load_apps()
        self.load_icons()
        self.initEvents()
        print("[lemapi] [INFO] [Desktop_activity.__init__] Activity started " \
            + "successfully !")

    def initEvents(self):
        lmgr = get_listener_manager()
        event = Event(exit)
        lmgr.add_key_down_event(event, K_LCTRL, K_ESCAPE)

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
            event = Event(self.run_app, app)
            self.view.widgets[wname].clickEvents.append(event)
            self.view.widgets["app_group"].add_app_widget( \
                self.view.widgets[wname])

    def run_app(self, app):
        print("[lemapi] [INFO] [Desktop_activity.run_app] Running app " \
            + "'%s' from lemapi desktop" % app.get_name())
        Instance.app = app
        app.load()
        app.run()

    def add_notif(self, title, msg):
        self.view.add_widget("notif", Notif_widget, (0, 0), title, msg)
