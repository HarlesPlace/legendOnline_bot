from core.daily_task import DailyTask
from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import wait_time, click, click_position
from utils.regions import *

class FantasyPub(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 8

    def _run_task(self):
        """
        Implementa a lógica para coletar bar da fantasia
        """
        print("Coletando bar da fantasia...")
        go_to_Interface("castle")
        if exists(r"legend_bot\images\fantasy_pub\fantasyPubButton.png", confidence=0.8, region=FULL_SCREEN):
            click(r"legend_bot\images\fantasy_pub\fantasyPubButton.png", region=FULL_SCREEN, confidence=0.8)
            if wait(r"legend_bot\images\fantasy_pub\magicCardsWindowBar.png", confidence=0.8, region=TOP_BAR, timeout=60):
                magic_cards_window_bar = find(r"legend_bot\images\fantasy_pub\magicCardsWindowBar.png", region=TOP_BAR, confidence=0.8)
                if click(r"legend_bot\images\fantasy_pub\pubButton.png", region=BOTTOM_BAR, confidence=0.8):
                    if wait(r"legend_bot\images\fantasy_pub\fantasyPubWindowBar.png", region=TOP_BAR, confidence=0.8, timeout=20):
                        pub_window_bar = find(r"legend_bot\images\fantasy_pub\fantasyPubWindowBar.png", region=TOP_BAR, confidence=0.8)
                        people_region=find(r"legend_bot\images\fantasy_pub\allPeopleBar.png", region=LEFT_SIDE, confidence=0.8)
                        people_list=[r"legend_bot\images\fantasy_pub\person1.png",
                                     r"legend_bot\images\fantasy_pub\person2.png",
                                     r"legend_bot\images\fantasy_pub\person3.png",
                                     r"legend_bot\images\fantasy_pub\person4.png",
                                     r"legend_bot\images\fantasy_pub\person5.png"
                                     ]
                        for person in people_list:
                            if click(person, region=people_region, confidence=0.9):
                                wait_time(1.5)
                                if exists(r"legend_bot\images\fantasy_pub\talkingIndicator.png", confidence=0.9, region=TOP_BAR):
                                    button=find(r"legend_bot\images\fantasy_pub\talkingButton.png", confidence=0.75, region=LEFT_SIDE)
                                    if not button:
                                        button=find(r"legend_bot\images\fantasy_pub\talkingButtonActivated.png", confidence=0.75, region=LEFT_SIDE)
                                    if button:
                                        wait_time(6)
                                        click_position(button)
                                        click_position(button)
                                        wait_time(2)
                                        click_position(button)
                                        wait_time(2)
                                click(r"legend_bot\images\fantasy_pub\returnButton.png", region=BOTTOM_RIGHT, confidence=0.8)
                                wait_time(2)
                        click(r"legend_bot\images\fantasy_pub\exitPubButton.png", confidence=0.8, region=pub_window_bar)
                        wait_time(2)
                click(r"legend_bot\images\fantasy_pub\exitMagicCardsButton.png", confidence=0.8, region=pub_window_bar)
                wait_time(2)
        return True