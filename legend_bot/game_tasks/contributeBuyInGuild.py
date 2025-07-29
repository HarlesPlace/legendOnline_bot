from core.daily_task import DailyTask
from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import wait_time, click, type_text
from utils.regions import *

itensTo_buy = [
    r"legend_bot\images\contribute_buy_in_guild\buy1.png",
    r"legend_bot\images\contribute_buy_in_guild\buy2.png",
    r"legend_bot\images\contribute_buy_in_guild\buy3.png",
    r"legend_bot\images\contribute_buy_in_guild\buy4.png",
    r"legend_bot\images\contribute_buy_in_guild\buy5.png",
    r"legend_bot\images\contribute_buy_in_guild\buy6.png",
    r"legend_bot\images\contribute_buy_in_guild\buy7.png",
    r"legend_bot\images\contribute_buy_in_guild\buy8.png",
    r"legend_bot\images\contribute_buy_in_guild\buy9.png",
    r"legend_bot\images\contribute_buy_in_guild\buy10.png",
    r"legend_bot\images\contribute_buy_in_guild\buy11.png",
    r"legend_bot\images\contribute_buy_in_guild\buy12.png",
    r"legend_bot\images\contribute_buy_in_guild\buy13.png",
    r"legend_bot\images\contribute_buy_in_guild\buy14.png",
    r"legend_bot\images\contribute_buy_in_guild\buy15.png",
    r"legend_bot\images\contribute_buy_in_guild\buy16.png",
]

class ContributeAndBuyInGuild(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 8

    def _run_task(self):
        """
        Implementa a lógica para contribuir a guilda e comprar itens na loja
        """
        print("Contribuindo a guilda...")
        go_to_Interface("castle") 
        if exists(r"legend_bot\images\contribute_buy_in_guild\systemMenuBar.png", confidence=0.5, region=BOTTOM_RIGHT):
            system_menu_region=find(r"legend_bot\images\contribute_buy_in_guild\systemMenuBar.png", confidence=0.5, region=BOTTOM_RIGHT)
            if click(r"legend_bot\images\contribute_buy_in_guild\guildButton.png", confidence=0.7, region=system_menu_region):
                if wait(r"legend_bot\images\contribute_buy_in_guild\guildWindowBar.png", confidence=0.6, region=TOP_BAR,timeout=120):
                    guildWindow_region=find(r"legend_bot\images\contribute_buy_in_guild\guildWindowBar.png", confidence=0.6, region=TOP_BAR)
                    if click(r"legend_bot\images\contribute_buy_in_guild\contributionButton.png", region=BOTTOM_LEFT, confidence=0.8):
                        if wait(r"legend_bot\images\contribute_buy_in_guild\contributionWindowBar.png", region=TOP_BAR, confidence=0.8, timeout=30):
                            contributionWindowBar_region = find(r"legend_bot\images\contribute_buy_in_guild\contributionWindowBar.png", region=TOP_BAR, confidence=0.8)
                            gold_region=find(r"legend_bot\images\contribute_buy_in_guild\goldValuePlace.png", confidence=0.85, region=FULL_SCREEN)
                            type_text("100000", 
                                    BeforeImage_path = r"legend_bot\images\contribute_buy_in_guild\goldValuePlace.png", 
                                    confidence=0.85)
                            wait_time(1)
                            click(r"legend_bot\images\contribute_buy_in_guild\contributeButton.png", region=gold_region, confidence=0.8)
                            wait_time(2)
                            if click(r"legend_bot\images\contribute_buy_in_guild\exitContributionButton.png", region=contributionWindowBar_region, confidence=0.8):
                                if wait(r"legend_bot\images\contribute_buy_in_guild\guildWindowBar.png", confidence=0.7, region=TOP_BAR,timeout=20):
                                    pass
                                else:
                                    print("Não foi possivel retornar ao hall da guilda após contribuir")
                                    return False
                    if guildWindow_region:
                        optionMenu_region=find(r"legend_bot\images\contribute_buy_in_guild\guildMenu.png", confidence=0.6, region=guildWindow_region)
                        if optionMenu_region:
                            if click(r"legend_bot\images\contribute_buy_in_guild\guildConstructionsButton.png", confidence=0.6, region=optionMenu_region):
                                if wait(r"legend_bot\images\contribute_buy_in_guild\constructionsInterface.png",region=FULL_SCREEN, confidence=0.95, timeout=30):
                                    construction_region=find(r"legend_bot\images\contribute_buy_in_guild\constructionsInterface.png",region=FULL_SCREEN, confidence=0.95)
                                    if click(r"legend_bot\images\contribute_buy_in_guild\storeButton.png", confidence=0.9, region=construction_region):
                                        if wait(r"legend_bot\images\contribute_buy_in_guild\storeWindowBar.png", region=TOP_BAR, confidence=0.8):
                                            storeWindow_region=find(r"legend_bot\images\contribute_buy_in_guild\storeWindowBar.png", region=TOP_BAR, confidence=0.8)
                                            count_pages = 0
                                            for item in itensTo_buy:
                                                if not self.running:
                                                    break
                                                if count_pages>=3:
                                                    print("Ocorreu algum erro, tetamos ir além das páginas da loja da guilda")
                                                    break
                                                if not exists(item, region=FULL_SCREEN, confidence=0.93):
                                                    print(f"Item {item} não encontrado.")
                                                    click(r"legend_bot\images\contribute_buy_in_guild\nextButton.png", region=BOTTOM_BAR, confidence=0.95)
                                                    wait_time(1)
                                                    count_pages+=1
                                                item_region=find(item, region=FULL_SCREEN, confidence=0.93)
                                                if item_region:
                                                    print(f"Item {item} encontrado, comprando...")
                                                    if click(r"legend_bot\images\contribute_buy_in_guild\buyButton.png", region=item_region, confidence=0.8):
                                                        if wait(r"legend_bot\images\contribute_buy_in_guild\inBuyIndicator.png", region=FULL_SCREEN, confidence=0.8, timeout=30):
                                                            try:
                                                                type_text("9999", 
                                                                        BeforeImage_path = r"legend_bot\images\contribute_buy_in_guild\quantityPlace.png", 
                                                                        AfterImage_path = r"legend_bot\images\contribute_buy_in_guild\confirmBuyButton.png", 
                                                                        confidence=0.8)
                                                            except:
                                                                click(r"legend_bot\images\contribute_buy_in_guild\confirmBuyButton.png", region=BOTTOM_BAR, confidence=0.8)
                                                            wait_time(6)
                                                else:
                                                    print(f"Item {item} não encontrado na loja.")
                                            click(r"legend_bot\images\contribute_buy_in_guild\exitStoreButton.png", confidence=0.8, region = storeWindow_region)
                    click(r"legend_bot\images\contribute_buy_in_guild\exitGuild.png", confidence=0.8, region=guildWindow_region)                                    
        return True

                                                
                                            