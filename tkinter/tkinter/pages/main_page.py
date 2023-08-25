import tkinter as tk
from widget.timer import Timer


class MainPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.study_timer = Timer(self, "Study", default=50)
        self.study_timer.grid(row=0, column=0)

        self.break_timer = Timer(self, "Break", default=10)
        self.break_timer.grid(row=1, column=0)

        self.banned_btn = tk.Button(self, text="banned programs", command=self.show_banned_page)
        self.banned_btn.grid(row=2, column=0)

        self.history_btn = tk.Button(self, text="History", command=self.show_history_page)
        self.history_btn.grid(row=2, column=1)

    def show_banned_page(self):
        self.parent.show_page(self.parent.banned_page)

    def show_history_page(self):
        self.parent.show_page(self.parent.history_page)
