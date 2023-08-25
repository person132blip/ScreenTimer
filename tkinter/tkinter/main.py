import tkinter as tk
import time
import psutil
import threading

from pages import MainPage, HistoryPage, BannedProgramsPage

from info_manager import InfoManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.info_manager = InfoManager.get_instance()
        self.info_manager.load_info()
        self.start_inspector()

        self.main_container = tk.Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        self.main_page = MainPage(self)
        self.banned_page = BannedProgramsPage(self)
        self.history_page = HistoryPage(self)

        self.current_page = self.main_page
        self.current_page.pack()
    
    def show_page(self, page: tk.Frame):
        self.current_page.pack_forget()
        self.current_page = page
        self.current_page.pack()

    def inspector_service(self):
        print(f"starting inspector service.\nHistory: {self.info_manager.info}")
        while True:
            # 1. aggregate all running process' name
            processes = {}
            for process in psutil.process_iter():
                processes[process.name()] = process

            # 2. Check if games are running
            for game_name, is_banned in self.info_manager.game_track_state.items():
                if game_name not in self.info_manager.info.keys():
                    self.info_manager.info[game_name] = {"seg": [], "state": False, "total": 0}
                gameobj = self.info_manager.info[game_name]

                if game_name in processes.keys():
                    if is_banned and not self.main_page.break_timer.is_running.is_set():
                        processes[game_name].kill()

                        if gameobj["state"]:
                            gameobj["seg"][-1][1] = time.time()
                            gameobj["state"] = False
                            self.info_manager.save_info()
                    else:
                        # game is running
                        if not gameobj["state"]:
                            gameobj["seg"].append([time.time(), None])
                            gameobj["state"] = True
                            self.info_manager.save_info()
                else:
                    # game is not running
                    if gameobj["state"]:
                        gameobj["seg"][-1][1] = time.time()
                        gameobj["total"] += gameobj["seg"][-1][1] - gameobj["seg"][-1][0]
                        gameobj["state"] = False
                        self.info_manager.save_info()
            # sleep for 1 second
            time.sleep(1)

    # called every time someone push the button
    def start_inspector(self):
        inspector_thread = threading.Thread(target=self.inspector_service, args=())
        inspector_thread.daemon = True
        inspector_thread.start()


if __name__ == '__main__':
    app = App()
    # app.geometry("300x300")
    app.mainloop()
