import tkinter as tk

import time
import random
from datetime import datetime, timedelta
from info_manager import InfoManager


def dtou(date: datetime):
    return time.mktime(date.timetuple())


def rgb_ccode(rgb):
    return "#%02x%02x%02x" % rgb


def all_round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def lower_round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
              x1, y1,
              x1, y1,
              x2, y1,
              x2, y1,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius]

    return canvas.create_polygon(points, **kwargs, smooth=True)


def upper_round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2,
              x2, y2,
              x1, y2,
              x1, y2,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)


int_to_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class StatCanvas(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.info_manager = InfoManager.get_instance()

        # get past 7 dates
        self.today = datetime.today()
        self.date_list = []
        for delta in range(6, -1, -1):
            self.date_list.append(self.today + timedelta(days=-1*delta))

        # get stats of past 7 days
        self.stat = []
        for date in self.date_list:
            start_datetime = datetime(date.year, date.month, date.day, 0, 0, 0, 0)
            end_datetime = start_datetime + timedelta(days=1)
            self.stat.append(self.info_manager.get_stat(dtou(start_datetime), dtou(end_datetime)))

        # get max play time
        # set color code
        self.color = {}
        self.max_playtime = 0
        for stat in self.stat:
            temp = 0
            for gamestat in stat:
                self.set_color(gamestat.name)
                temp += gamestat.total
            if temp > self.max_playtime:
                self.max_playtime = temp

        # canvas parameters
        self.height = 400
        self.width = 700

        self.bar_width_perc = 0.7
        self.bar_height_perc = 0.9
        self.slot_width = self.width / 7

        self.bar_width = self.slot_width * self.bar_width_perc
        self.bar_max_height = self.height * self.bar_height_perc

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white", bd=2)
        self.canvas.pack()

        # draw bars
        for idx, stat in enumerate(self.stat):
            prev_height = 0
            for game_i, gamestat in enumerate(stat):
                playtime = gamestat.total
                game_name = gamestat.name

                if game_i == 0 and len(stat) == 1:
                    prev_height = self.draw_bar(idx, prev_height, playtime, game_name, 3)
                elif game_i == 0:
                    prev_height = self.draw_bar(idx, prev_height, playtime, game_name, 2)
                elif game_i == len(stat) -1:
                    prev_height = self.draw_bar(idx, prev_height, playtime, game_name, 1)
                else:
                    prev_height = self.draw_bar(idx, prev_height, playtime, game_name, 0)

        # draw dates
        for idx, date in enumerate(self.date_list):
            day = int_to_day[date.weekday()]
            self.draw_text(idx, day)

    def draw_text(self, idx, day):
        x = (self.slot_width * idx) + (self.slot_width / 2)
        y = int(self.height * (1-self.bar_height_perc) / 2)
        self.canvas.create_text(x, y, text=day, fill="black", font=('Helvetica 15'))

    def draw_bar(self, idx, prev_height, playtime, game_name, shape):
        lx = (self.slot_width * idx) + (self.slot_width / 2) - (self.bar_width / 2)
        rx = (self.slot_width * idx) + (self.slot_width / 2) + (self.bar_width / 2)

        if self.max_playtime == 0:
            bar_height = 0
        else:
            bar_height = (playtime / self.max_playtime) * self.bar_max_height
        ly = self.height - (bar_height + prev_height)
        ry = self.height - prev_height

        color = rgb_ccode(self.color[game_name])
        if shape == 0:
            self.canvas.create_rectangle(int(lx), int(ly), int(rx), int(ry), fill=color)
        elif shape == 1:
            upper_round_rectangle(self.canvas, int(lx), int(ly), int(rx), int(ry), fill=color)
        elif shape == 2:
            lower_round_rectangle(self.canvas, int(lx), int(ly), int(rx), int(ry), fill=color)
        else:
            all_round_rectangle(self.canvas, int(lx), int(ly), int(rx), int(ry), fill=color)

        return bar_height + prev_height

    def set_color(self, name):
        if name not in self.color.keys():
            r = random.randint(100, 256)
            g = random.randint(100, 256)
            b = random.randint(100, 256)
            self.color[name] = (r, g, b)
