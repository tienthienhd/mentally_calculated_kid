#!/usr/bin/python3
import os.path
import pathlib
import pickle
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

        builder.import_variables(self, ["n", "min", "max", "time", "operation"])

        builder.connect_callbacks(self)

        self.values = []
        self.ops = []
        self.load_config()

    def load_config(self):
        if os.path.exists('config.pkl'):
            config = pickle.load(open('config.pkl', 'rb'))
            if isinstance(config, dict):
                self.n.set(config.get('n', 5))
                self.min.set(config.get('min', -99999))
                self.max.set(config.get('max', 99999))
                self.time.set(config.get('time', 10))
                self.operation.set(config.get('operation', 10))
                return
        self.n.set(5)
        self.min.set(-99999)
        self.max.set(99999)
        self.time.set(10)
        self.operation.set('+')

    def save_config(self):
        pickle.dump({
            'n': self.n.get(),
            'min': self.min.get(),
            'max': self.max.get(),
            'time': self.time.get(),
            'operation': self.operation.get(),
        }, open('config.pkl', 'wb'))

    def run(self):
        self.mainwindow.mainloop()

    def start_run_test(self):
        self.values.clear()
        self.ops.clear()
        builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        frame2 = builder.get_object('learning', self.mainwindow)
        self.number = None
        self.step_operation = None
        builder.import_variables(self, ["number", "step_operation"])
        builder.connect_callbacks(self)
        self.thread_test = Thread(target=self.run_test)
        self.thread_test.start()

    def run_test(self):
        i = 0
        total_time = self.time.get()
        n = self.n.get()
        min = self.min.get()
        max = self.max.get()
        operation = self.operation.get()
        time_to_sleep = total_time / (n + 1)
        self.values = [random.randint(min, max) for _ in range(n)]
        self.ops = [''] + [operation[random.randint(0, len(operation) - 1)] for _ in range(n - 1)]
        for i in range(n):
            self.number.set(self.values[i])
            if i != n:
                self.step_operation.set(self.ops[i])
            try:
                time.sleep(time_to_sleep)
            except Exception as e:
                continue
        self.step_operation.set('')
        self.number.set("=")
        try:
            time.sleep(time_to_sleep)
        except Exception as e:
            pass

    def show_result(self):
        elements = []
        for i in range(len(self.values)):
            elements.append(str(self.values[i]))
            elements.append(self.ops[i-1])

        equation = " ".join(elements)
        print(equation)
        result = eval(equation)
        self.number.set(result)


if __name__ == "__main__":
    app = AppApp()
    app.run()
