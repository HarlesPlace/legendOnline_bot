from core.daily_task import DailyTask

from utils.general_use import open_map, by_map_go_to
from utils.screenVision import exists, wait, find, list_all, wait_until_disappear
from utils.actions import wait_time, click, click_position
from utils.regions import *

class GuardSearch(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 5

    def _run_task(self):
        """
        Implementa a lógica para coletar os guardioes procurados.
        """
        print("Coletando guardioes procurados...")

        if open_map():
            if by_map_go_to("GuardiaoCeleste"):
                if wait(r"legend_bot\images\guard_search\interfaceIndicator.png", confidence=0.8, timeout=60, region=FULL_SCREEN):
                    searchGuard_region = find(r"legend_bot\images\guard_search\interfaceIndicator.png", confidence=0.8,region=FULL_SCREEN)
                    click(r"legend_bot\images\guard_search\guardSearchButton.png", region=searchGuard_region, confidence=0.8)
                    if wait(r"legend_bot\images\guard_search\mainWindowBar.png", confidence=0.8, timeout=30, region=TOP_BAR):
                        battles = list_all(r"legend_bot\images\guard_search\battleIndicator.png", confidence=0.8)
                        chests= list_all(r"legend_bot\images\guard_search\chest.png", confidence=0.8)
                        for battle in battles:
                            if not self.running:
                                break
                            click_position(battle)
                            if wait(r"legend_bot\images\guard_search\battleWindowBar.png", confidence=0.8, timeout=30, region=TOP_BAR):
                                if click(r"legend_bot\images\guard_search\challengeButton.png", region=BOTTOM_BAR, confidence=0.6):
                                    if wait(r"legend_bot\images\guard_search\inBattleIndicator.png", timeout=30, region=BOTTOM_RIGHT, confidence=0.8):
                                        if wait_until_disappear(r"legend_bot\images\guard_search\inBattleIndicator.png", timeout=120, region=BOTTOM_RIGHT, confidence=0.8):
                                            if wait(r"legend_bot\images\guard_search\mainWindowBar.png", confidence=0.8, timeout=30, region=TOP_BAR):
                                                pass
                                            else:
                                                print("[Guardião Procurado] Não retornou a tela inicial após a batalha")
                                                return False
                                        else:
                                            print("[Guardião Procurado] Houve um erro, permaneceu em batalha mesmo após o encerramento")
                                            return False        
                                    else:
                                        print("[Guardião Procurado] Esperado entrar em batalha, mas não aconteceu")
                                        return False
                                else:
                                    print("[Guardião Procurado] Erro ao achar botão de batalha")
                                    return False
                        for chest in chests:
                            if not self.running:
                                break
                            click_position(chest)
                            wait_time(3)
                            if exists(r"legend_bot\images\guard_search\inTowerWindowBar.png", confidence=0.8, region=TOP_BAR):
                                region=find(r"legend_bot\images\guard_search\inTowerWindowBar.png", confidence=0.8, region=TOP_BAR)
                                click(r"legend_bot\images\guard_search\exitTowerButton.png", region=region, confidence=0.8)
                                wait_time(3)

                        region=find(r"legend_bot\images\guard_search\mainWindowBar.png", confidence=0.8, region=TOP_BAR)
                        print("aaaaaaaaaaaaaaaaaa")
                        click(r"legend_bot\images\guard_search\searchGuardExitButton.png", region=region, confidence=0.8)
                        print("bbbbbbbbbbbbbbbbb")
                        wait_time(3)
                        return True
                    else:
                        print("[Guardião Procurado] Não entrou na interface do guardião procurado")
                        return False
                else:
                    print("[Guardião Procurado] não apareceu interface para entrada")
                    return False
                