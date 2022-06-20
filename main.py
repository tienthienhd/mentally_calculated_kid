#!/usr/bin/python3
import pathlib
import time
from threading import Thread

import pygubu
import tkinter as tk
import random

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "app.ui"


class AppApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("setting", master)
        self.master = master

        self.n = None
        self.min = None
        self.max = None
        self.time = None
        self.operation = None

        builder.import_variables(self, ["n", "min", "max", "time", "operation", "number"])

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def start_run_test(self):
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        frame2 = builder.get_object('learning', self.mainwindow)
        self.number = None
        builder.import_variables(self, ["number"])
        builder.connect_callbacks(self)
        self.thread_test = Thread(target=self.run_test)
        self.thread_test.start()

    def run_test(self):
        i = 0
        total_time = self.time.get()
        n = self.n.get()
        min = self.min.get()
        max = self.max.get()
        time_to_sleep = total_time / (n + 1)
        show_chars = [random.randint(min, max) for _ in range(n)]
        for i in range(n):
            self.number.set(show_chars[i])
            try:
                time.sleep(time_to_sleep)
            except Exception as e:
                continue
        self.number.set("=")
        try:
            time.sleep(time_to_sleep)
        except Exception as e:
            pass
        sum_value = sum(show_chars)
        self.number.set(sum_value)


if __name__ == "__main__":
    app = AppApp()
    app.run()
