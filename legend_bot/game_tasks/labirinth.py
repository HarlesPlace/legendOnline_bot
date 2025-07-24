from core.daily_task import DailyTask
from utils.general_use import go_to_Interface, open_map, by_map_go_to, move_mouse_outside_screen
from utils.screenVision import exists, wait, find, list_all, check_right, wait_until_disappear
from utils.actions import wait_time, click, click_position
from utils.regions import *
from utils.OCR import extract_text_right_of_image, extract_text_from_position

class Labirinth(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 8

    def _run_task(self):
        """
        Implementa a lógica para coletar XP farm
        """
        print("Coletando XP farm...")
        go_to_Interface("castle") 