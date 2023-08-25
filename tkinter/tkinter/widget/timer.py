import tkinter as tk
import threading
import time


class Timer(tk.Frame):
    def __init__(self, parent, name, default):
        tk.Frame.__init__(self, parent)
        self.name = name
        self.parent = parent
        self.is_running = threading.Event()

        self.default = default

        self.sv = tk.StringVar()
        self.sv.trace("w", self.txt_changed)
        self.entry = tk.Entry(self, textvariable=self.sv)
        self.entry.insert(tk.END, f"{default}")
        self.entry.grid(row=0, column=0)

        if self.name == "Break":
            self.btn = tk.Button(self, text=self.btn_txt(), command=self.button_clicked, state=tk.DISABLED)
        else:
            self.btn = tk.Button(self, text=self.btn_txt(), command=self.button_clicked)

        self.btn.grid(row=0, column=1)

        self.timer_thread = None

    def button_clicked(self):
        if not self.is_running.is_set():
            self.is_running.set()
            self.timer_thread = threading.Thread(target=self.start_timer, args=())
            self.timer_thread.daemon = True
            self.timer_thread.start()
        else:
            self.is_running.clear()
        self.btn.config(text=self.btn_txt())

    def txt_changed(self, *args):
        if self.name == "Study":
            try:
                current_time = int(self.entry.get())
                if current_time == 0:
                    # enable break timer's btn
                    self.parent.break_timer.btn.config(state=tk.NORMAL)
                else:
                    # disable break timer's btn
                    self.parent.break_timer.btn.config(state=tk.DISABLED)
            except:
                pass

    def start_timer(self):
        while self.is_running.is_set():
            time.sleep(1)

            try:
                current_time = int(self.entry.get())

                if current_time > 0:
                    self.entry.delete(0, tk.END)
                    self.entry.insert(tk.END, f"{current_time - 1}")
                elif current_time == 0:
                    self.is_running.clear()
                    self.btn.config(text=self.btn_txt())
                else:
                    self.entry.delete(0, tk.END)
                    self.entry.insert(tk.END, f"{self.default}")
            except:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, f"{self.default}")

    def btn_txt(self):
        if self.is_running.is_set():
            return f"{self.name} Stop"
        else:
            return f"{self.name} Start"
