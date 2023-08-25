import tkinter as tk

from info_manager import InfoManager


class BannedRowView(tk.Frame):
    def __init__(self, parent, game_name, is_banned):
        tk.Frame.__init__(self, parent)
        self.game_name = game_name
        self.is_banned = tk.IntVar(value=int(is_banned))
        self.btn = tk.Checkbutton(self, text=self.game_name, variable=self.is_banned, onvalue=1, offvalue=0, command=self.update)
        self.btn.pack()

    def update(self):
        state = self.is_banned.get()
        InfoManager.get_instance().game_track_state[self.game_name] = state == 1


class BannedListVeiw(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        for i, (game_name, is_banned) in enumerate(InfoManager.get_instance().game_track_state.items()):
            row_view = BannedRowView(self, game_name, is_banned)
            row_view.grid(row=i, column=0)


class BannedProgramsPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.list_view = BannedListVeiw(self)
        self.back_btn = tk.Button(self, text="back", command=self.show_main_pages)

        self.list_view.grid(row=0, column=0)
        self.back_btn.grid(row=0, column=1)

    def show_main_pages(self):
        self.parent.show_page(self.parent.main_page)


