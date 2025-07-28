from core.repeatable_task import RepeatableTask
from datetime import timedelta

from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find, list_all
from utils.actions import wait_time, click, click_with_offset
from utils.regions import *

class GuildTreasure(RepeatableTask):
    def __init__(self):
        super().__init__()
        self.interval = timedelta(minutes=70)
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 3

    def _run_task(self):
        """
        Implementa a lógica para coletar tesouro da guilda
        """
        print("Coletando tesoura da guilda...")
        go_to_Interface("castle") 
        if exists(r"legend_bot\images\guild_treasure\systemMenuBar.png", confidence=0.5, region=BOTTOM_RIGHT):
            system_menu_region=find(r"legend_bot\images\guild_treasure\systemMenuBar.png", confidence=0.5, region=BOTTOM_RIGHT)
            if click(r"legend_bot\images\guild_treasure\guildButton.png", confidence=0.7, region=system_menu_region):
                if wait(r"legend_bot\images\guild_treasure\guildWindowBar.png", confidence=0.6, region=TOP_BAR,timeout=120):
                    guildWindow_region=find(r"legend_bot\images\guild_treasure\guildWindowBar.png", confidence=0.6, region=TOP_BAR)
                    if guildWindow_region:
                        optionMenu_region=find(r"legend_bot\images\guild_treasure\guildMenu.png", confidence=0.6, region=guildWindow_region)
                        if optionMenu_region:
                            if click(r"legend_bot\images\guild_treasure\guildEventsBarButton.png", confidence=0.6, region=optionMenu_region):
                                if wait(r"legend_bot\images\guild_treasure\guildTreasureAcessRegion.png",region=FULL_SCREEN, confidence=0.95, timeout=30):
                                    if click_with_offset(r"legend_bot\images\guild_treasure\guildTreasureAcessRegion.png",offset=(100,100), confidence=0.9, region=FULL_SCREEN):
                                        if wait(r"legend_bot\images\guild_treasure\guildTreasureWindowBar.png", region=TOP_BAR, confidence=0.8, timeout=60):
                                            treasure_access_region =find(r"legend_bot\images\guild_treasure\guildTreasureWindowBar.png", region=FULL_SCREEN, confidence=0.9)
                                            option_regions=find(r"legend_bot\images\guild_treasure\optionsMenu.png", region=LEFT_SIDE, confidence=0.8)
                                            if exists(r"legend_bot\images\guild_treasure\escavateButton.png", region=FULL_SCREEN, confidence=0.9):
                                                click(r"legend_bot\images\guild_treasure\escavateButton.png", region=FULL_SCREEN, confidence=0.9)
                                                wait_time(2)
                                            if click(r"legend_bot\images\guild_treasure\myTreasureButton.png", confidence=0.85, region=option_regions):
                                                wait_time(2)
                                                if exists(r"legend_bot\images\guild_treasure\askForHelpButton.png", region=FULL_SCREEN, confidence=0.8):
                                                    click(r"legend_bot\images\guild_treasure\askForHelpButton.png", region=FULL_SCREEN, confidence=0.8)
                                                    wait_time(2)
                                                if exists(r"legend_bot\images\guild_treasure\colectMyTeasureButton.png", confidence=0.9, region=FULL_SCREEN):
                                                    click(r"legend_bot\images\guild_treasure\colectMyTeasureButton.png", region=FULL_SCREEN, confidence=0.9)
                                                    wait_time(2)
                                            if click(r"legend_bot\images\guild_treasure\listOfHelpButton.png", confidence=0.85, region=option_regions):
                                                wait_time(2)
                                                if exists(r"legend_bot\images\guild_treasure\helpButton.png", region=FULL_SCREEN, confidence=0.8):
                                                    click(r"legend_bot\images\guild_treasure\helpButton.png", region=FULL_SCREEN, confidence=0.8)
                                                    wait_time(2)
                                                if exists(r"legend_bot\images\guild_treasure\colectMyTeasureButton.png", confidence=0.9, region=FULL_SCREEN):
                                                    click(r"legend_bot\images\guild_treasure\colectMyTeasureButton.png", region=FULL_SCREEN, confidence=0.9)
                                                    wait_time(2)
                                            click(r"legend_bot\images\guild_treasure\exitTreasure.png", region=treasure_access_region, confidence=0.8)
                                            wait_time(2)
                        else:
                            print("[Tesouro da Guilda] Não foi possível encontrar o menu de opções.")
                            return False
                    click(r"legend_bot\images\guild_treasure\exitGuild.png", region=guildWindow_region, confidence=0.8)
        return True