# -*- coding: utf-8 -*-

"""
Provides classes to manage delayed functions or asynchronous running.

Created on 20/01/2019
"""

from lemapi.event_manager import Event

__author__ = "Julien Dubois"
__version__ = "0.1.0"


class Task_manager(object):
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, task):
        if name not in self.tasks:
            self.tasks[name] = task

    def remove_task(self, name):
        if name in self.tasks:
            self.tasks.pop(name)

    def update(self, deltatime):
        for name, task in tuple(self.tasks.items()):
            if task.obsolete:
                self.tasks.pop(name)
            else:
                task.update(deltatime)


class Task_delay(Event):
    def __init__(self, delay, fct, *args, **kwargs):
        self.delay = delay
        self.elapsed_time = 0
        super().__init__(fct, *args, **kwargs)

    def update(self, deltatime):
        self.elapsed_time += deltatime

        if self.elapsed_time >= self.delay:
            self.call()


class Analog_task_delay(Task_delay):
    def __init__(self, delay, fct, *args, **kwargs):
        self.value = 0
        super().__init__(delay, fct, *args, **kwargs)

    def update(self, deltatime):
        self.elapsed_time += deltatime
        self.value += deltatime / self.delay

        if self.value > 1:
            self.value = 1

        if self.elapsed_time >= self.delay:
            self.obsolete = True
        else:
            self.call(self.value)
            self.obsolete = False
