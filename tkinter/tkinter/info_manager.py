from typing import List
import os
import json

ROOT = os.path.dirname(os.path.realpath(__file__))
INFO_PATH = os.path.join(ROOT, "info.json")


class GameStat:
    def __init__(self, name, seg, color):
        self.name = name
        self.seg = seg
        self.color = color
        self.total = 0
        for start_time, end_time in self.seg:
            self.total += (end_time - start_time)


class InfoManager(object):
    __instance = None

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = InfoManager()
        return cls.__instance

    def __init__(self):
        if not InfoManager.__instance:
            self.game_list = ["League of Legend", "Overwatch", "Elden Ring", "Safari"]
            self.game_track_state = {}
            for game_name in self.game_list:
                self.game_track_state[game_name] = True
            self.info = {}
        else:
            print("Object already created")

    def load_info(self):
        if os.path.exists(INFO_PATH):
            with open(INFO_PATH, "r") as f:
                self.info = json.load(f)

    def save_info(self):
        json_string = json.dumps(self.info)
        with open(INFO_PATH, "w") as f:
            f.write(json_string)

    def get_stat(self, start_time: int, end_time: int) -> List[GameStat]:
        stat_list = []
        for game_name in self.info.keys():
            new_seg = []
            seg = self.info[game_name]["seg"]
            for temp_start, temp_end in seg:
                is_intersection = not (temp_start > end_time or temp_end < start_time)
                if is_intersection:
                    new_seg.append([max(start_time, temp_start), min(end_time, temp_end)])
            if len(new_seg) > 0:
                stat_list.append(GameStat(game_name, new_seg, "black"))
        return stat_list


manager = InfoManager()
