# -*- coding: utf-8 -*-

from lemapi_desktop.widget import App_group, Clock_widget, Splash_labyrinth

__author__ = "Julien Dubois"
__version__ = "0.1.0"

from lemapi.api import get_gui, get_listener_manager, start_app, get_theme_color, get_task_manager, get_activity
from lemapi.constants import Path
from lemapi.event_manager import Event
from lemapi.task_manager import Analog_task_delay, Task_delay
from lemapi.util import read_json, resize_image
from lemapi.view import View
from lemapi.widget import Image_widget, Text

from os.path import join
from pygame.locals import K_UP, K_DOWN, K_RETURN


class Splash_view(View):
    def init_widgets(self):
        self.add_toast("Demarrage de LemAPI...", textColor=(75, 75, 75, 255))

    def create_labyrinth(self):
        w, h = get_gui().get_size()
        self.add_widget("labyrinth_widget", Splash_labyrinth, (w // 2, h // 2), \
            size=(h * 0.8, h * 0.8), anchor=(0, 0))

    def create_logo(self):
        w, h = get_gui().get_size()
        path = join(Path.IMAGES, "splash", "lem_logo.png")

        self.add_widget("title_image", Image_widget, (w // 2, h // 2), \
            path, size=(h * 0.4, h * 0.4), anchor=(0, 0), alphaChannel=False, \
            transparentColor=(0, 0, 0))
        self.widgets["title_image"].set_opacity(0)

    def update(self):
        get_gui().draw_background_color((255, 255, 255))
        super().update()


class Desktop_view(View):
    def __init__(self):
        super().__init__()
        self.temp_screen_surface = None
        self.app_animation_surface = None
        self.in_animation = False

    def init_widgets(self):
        w, h = get_gui().get_size()
        bg_path = join(Path.IMAGES, "background", get_theme_color() + ".png")

        self.add_widget("background_image", Image_widget, (w // 2, h // 2), bg_path, size=(w, h), anchor=(0, 0))
        self.add_widget("app_group", App_group, (w, h // 2), anchor=(0, 0))
        self.add_widget("clock_widget", Clock_widget, (w * 0.1, h * 0.2), anchor=(-1, 0))

    def init_events(self):
        lm = get_listener_manager()
        w = self.widgets["app_group"]
        event = Event(w.previous_app)
        lm.km.add_key_down_event(event, K_DOWN)
        lm.cm.add_joy_down_event(event)
        event = Event(w.next_app)
        lm.km.add_key_down_event(event, K_UP)
        lm.cm.add_joy_up_event(event)
        event = Event(w.click_app)
        lm.km.add_key_down_event(event, K_RETURN)
        lm.cm.add_button_pressed_event(event, "button_a")

        for widget in w.app_widgets:
            event = Event(get_activity().click_app, widget.app)
            widget.endClickEvents.append(event)

    def add_app(self, widget_name):
        if widget_name in self.widgets:
            self.widgets["app_group"].add_app_widget(self.widgets[widget_name])

    def reset_angle(self):
        self.widgets["app_group"].reset_angle()

    def update(self):
        if not self.in_animation:
            super().update()

    def start_appopen_transition(self, app):
        task = Analog_task_delay(0.3, self.update_app_transition)
        gui = get_gui()
        splash_path = app.get_splash_path()
        gui.load_image(splash_path)

        self.in_animation = True
        self.temp_screen_surface = gui.get_current_surface()
        self.app_animation_surface = gui.get_image(splash_path)
        get_task_manager().add_task("activity_transition_animation", task)

    def update_app_transition(self, state):
        gui = get_gui()
        gui.draw_background_color((0, 0, 0))

        if state <= 0.25:
            h = (1 - state * 4) * 480
            surface = resize_image(self.temp_screen_surface, (800, h))
            gui.draw_image(surface, (0, 240 - h/2))
            gui.draw_line((255, 255, 255), (0, 240 - h/2), (800, 240 - h/2), width=5)
            gui.draw_line((255, 255, 255), (0, 240 + h/2), (800, 240 + h/2), width=5)
        elif state <= 0.5:
            w = (1 - (state - 0.25) * 4) * 800
            gui.draw_line((255, 255, 255), (400 - w/2, 240), (400 + w/2, 240), width=5)
        elif state <= 0.75:
            w = (state - 0.5) * 4 * 800
            gui.draw_line((255, 255, 255), (400 - w/2, 240), (400 + w/2, 240), width=5)
        else:
            h = (state - 0.75) * 4 * 480
            surface = resize_image(self.app_animation_surface, (800, h))
            gui.draw_image(surface, (0, 240 - h/2))
            gui.draw_line((255, 255, 255), (0, 240 - h/2), (800, 240 - h/2), width=5)
            gui.draw_line((255, 255, 255), (0, 240 + h/2), (800, 240 + h/2), width=5)

    def start_appclose_transition(self):
        task = Analog_task_delay(0.3, self.update_app_transition)
        gui = get_gui()
        splash_path = join(Path.IMAGES, "background", "{theme_color}.png")
        gui.load_image(splash_path)

        self.in_animation = True
        self.temp_screen_surface = gui.get_current_surface()
        self.app_animation_surface = gui.get_image(splash_path)
        get_task_manager().add_task("activity_transition_animation", task)

        def end_animation():
            self.in_animation = False

        get_task_manager().add_task("end_activity_transition", Task_delay(0.35, end_animation))

    def set_quit_view(self):
        w, h = get_gui().get_size()
        path = join(Path.IMAGES, "quit_view.png")
        self.add_widget("quit_view_image", Image_widget, (w*0.5, h*0.5), path, size=(800, 480), anchor=(0, 0))