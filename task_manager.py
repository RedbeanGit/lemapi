# -*- coding: utf-8 -*-

"""
Provides classes to manage delayed functions or asynchronous running.

Created on 20/01/2019
"""

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import threading


class Task_manager(object):
    def __init__(self):
        self.threads = []

    def run_async(self, fct, *args, **kwargs):
        thread = threading.Thread(target=fct, args=args, kwargs=kwargs)
        self.threads.append(thread)
        thread.start()
