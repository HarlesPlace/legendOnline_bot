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
        Implementa a lógica para coletar labirinto
        """
        print("Coletando labirinto...")
        go_to_Interface("castle")
        if exists(r"legend_bot\images\labirinth\labirinthCastleButton.png", confidence=0.8, region=BOTTOM_BAR):
            castle_button_place=find(r"legend_bot\images\labirinth\labirinthCastleButton.png", confidence=0.8, region=BOTTOM_BAR)
            labirinths=[r"legend_bot\images\labirinth\lab1Button.png",
                        r"legend_bot\images\labirinth\lab2Button.png",
                        r"legend_bot\images\labirinth\lab3Button.png"]
            for lab in labirinths:
                for i in range(3):
                    if not exists(r"legend_bot\images\labirinth\window.png", region=TOP_BAR, confidence=0.8):
                        try:
                            click_position(castle_button_place)
                        except:
                            click(r"legend_bot\images\labirinth\labirinthCastleButton.png", confidence=0.8, region=BOTTOM_BAR)
                    if wait(r"legend_bot\images\labirinth\window.png", region=TOP_BAR, confidence=0.8, timeout=60):
                        if exists(lab, confidence=0.8, region=LEFT_SIDE):
                            click(lab, confidence=0.8, region=LEFT_SIDE)
                        lab_menu_region = find(r"legend_bot\images\labirinth\labMenu.png", region=FULL_SCREEN, confidence=0.5)
                        if exists(r"legend_bot\images\labirinth\canNotDOindicator.png", confidence=0.95, region=lab_menu_region):
                            break
                        canDoIndicator = exists(r"legend_bot\images\labirinth\canDOindicator.png", confidence=0.95, region=lab_menu_region)
                        continueBotIndicator = exists(r"legend_bot\images\labirinth\continueBOTindicator.png", confidence=0.95, region =lab_menu_region)
                        print(f"Labirinth {i} - canDoIndicator: {canDoIndicator}, continueBotIndicator: {continueBotIndicator}")
                        if (canDoIndicator or continueBotIndicator):
                            if canDoIndicator:
                                if click(r"legend_bot\images\labirinth\initLab.png", region=lab_menu_region, confidence=0.8):
                                    wait_time(5)
                                    if exists(r"legend_bot\images\labirinth\buyKeyIndicator.png", region=FULL_SCREEN, confidence=0.8):
                                        buy_region=find(r"legend_bot\images\labirinth\buyKeyIndicator.png", region=FULL_SCREEN, confidence=0.8)
                                        click(r"legend_bot\images\labirinth\exitBuyKey.png", region=buy_region, confidence=0.8)
                                        wait_time(2)
                                        dontUseKey=find(r"legend_bot\images\labirinth\labKeyUseButton.png", region=lab_menu_region, confidence=0.9)
                                        click_position(dontUseKey)
                                        wait_time(1)
                                        click(r"legend_bot\images\labirinth\initLab.png", region =lab_menu_region, confidence=0.9)
                            elif continueBotIndicator:
                                click(r"legend_bot\images\labirinth\continueBOTbutton.png", region=lab_menu_region, confidence=0.9)
                                wait_time(2)
                                print("/////////////////////////////////")
                            aaa=exists(r"legend_bot\images\labirinth\botWindowBar.png", region=FULL_SCREEN, confidence=0.7)
                            print(f"Bot window exists: {aaa}")
                            if wait(r"legend_bot\images\labirinth\botWindowBar.png", region=FULL_SCREEN, confidence=0.7, timeout=30):
                                bot_bar_region=find(r"legend_bot\images\labirinth\botWindowBar.png", region=FULL_SCREEN, confidence=0.8)
                                click(r"legend_bot\images\labirinth\initBOTbutton.png", region=RIGHT_SIDE, confidence=0.8)
                                wait_time(5)
                                print("aaaaaaaaaaaaaaaaaaaaaaaaa")
                                if exists(r"legend_bot\images\labirinth\botInExecusionIndicator.png", region=BOTTOM_BAR, confidence=0.8):
                                    menu_region=find(r"legend_bot\images\labirinth\botInExecusionIndicator.png", region=BOTTOM_BAR, confidence=0.8)
                                    click(r"legend_bot\images\labirinth\botAcelerateButton.png", region=menu_region, confidence=0.8)
                                    if wait(r"legend_bot\images\labirinth\botConcludedIndicator.png", region=BOTTOM_LEFT, confidence=0.8,timeout=200):
                                        click(r"legend_bot\images\labirinth\botConcludeButton.png", region=menu_region, confidence=0.8)
                                        wait_time(2)
                            else:
                                print("bbbbbbbbbbbbbbbbbbbbbbbb")
                        elif exists(r"legend_bot\images\labirinth\lastStepIndicator.png", confidence=0.9, region=lab_menu_region):
                            if click(r"legend_bot\images\labirinth\doLastStepButton.png", region=lab_menu_region, confidence=0.9):
                                if wait(r"legend_bot\images\labirinth\inLastStepIndicator.png", region=TOP_LEFT, confidence=0.85, timeout=160):
                                    if exists(r"legend_bot\images\labirinth\autoFightButton.png", region=TOP_LEFT, confidence=0.85):
                                        click(r"legend_bot\images\labirinth\autoFightButton.png", region=TOP_LEFT, confidence=0.85)
                                        if wait(r"legend_bot\images\labirinth\inCombatIndicator.png", region=TOP_RIGHT, confidence=0.8, timeout=120):
                                            if wait_until_disappear(r"legend_bot\images\labirinth\inCombatIndicator.png", region=TOP_RIGHT, confidence=0.8, timeout=150):
                                                if wait(r"legend_bot\images\labirinth\gainsWindowBar.png", region=TOP_BAR, confidence=0.8, timeout=120):
                                                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                                    gains_region=find(r"legend_bot\images\labirinth\gainsWindowBar.png", region=TOP_BAR, confidence=0.8)
                                                    click(r"legend_bot\images\labirinth\exitGainButton.png", region=TOP_BAR, confidence=0.8)
                                                    wait_time(3)
                                                else:
                                                    print("??????????????????????????????")
            if exists(r"legend_bot\images\labirinth\window.png", region=TOP_BAR, confidence=0.8):
                windowBar_region=find(r"legend_bot\images\labirinth\window.png", region=TOP_BAR, confidence=0.8)
                click(r"legend_bot\images\labirinth\exitLabButton.png", region=windowBar_region, confidence=0.8)
            return True

                                     




