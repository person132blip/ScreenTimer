import tkinter as tk

from widget.stat_canvas import StatCanvas


class HistoryPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.stat_canvas = StatCanvas(self)
        self.stat_canvas.pack()
