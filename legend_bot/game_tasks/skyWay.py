from core.daily_task import DailyTask

from utils.general_use import open_map, by_map_go_to
from utils.screenVision import exists, wait, find, list_all, wait_until_disappear
from utils.actions import wait_time, click, hover_position
from utils.regions import *
from utils.OCR import extract_text_from_position

class SkyWay(DailyTask):
    def __init__(self):
        super().__init__()
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 6

    def _run_task(self):
        if open_map():
            if by_map_go_to("CaminhoCeu"):
                if wait(r"legend_bot\images\sky_way\interfaceIndicator.png", confidence=0.8, timeout=30, region=FULL_SCREEN):
                    arenaPET_region = find(r"legend_bot\images\sky_way\interfaceIndicator.png", confidence=0.8,region=FULL_SCREEN)
                    click(r"legend_bot\images\sky_way\skyWayButton.png", region=arenaPET_region, confidence=0.8)
                    if wait(r"legend_bot\images\sky_way\windowIndicator.png", confidence=0.8, timeout=30, region=TOP_BAR):
                        results_position=list_all(r"legend_bot\images\sky_way\chest.png", confidence=0.89)
                        engine=True
                        i=0
                        if exists(r"legend_bot\images\sky_way\skyWayTotalyCompletedIndicator.png", confidence=0.95, region= TOP_LEFT):
                            totalyCompleted=True
                        else:
                            totalyCompleted=False
                        while engine and (i<len(results_position))and self.running:
                            hover_position(results_position[i])
                            wait_time(3)
                            if exists(r"legend_bot\images\sky_way\greyChalengeButton.png",confidence=0.9, region=FULL_SCREEN) or totalyCompleted:
                                engine=False
                                click(r"legend_bot\images\sky_way\searchButton.png", region=FULL_SCREEN, confidence=0.9)
                                if wait(r"legend_bot\images\sky_way\inWayIndicator.png", confidence=0.8, timeout=30, region=BOTTOM_RIGHT):
                                    while self.running:
                                        try:
                                            conclusionPercentage=extract_text_from_position(position=find(r"legend_bot\images\sky_way\inWayIndicator.png", confidence=0.8, region=BOTTOM_RIGHT),
                                                                                        offset=(-425, 25, 100, 50),invert=True, debug=True, only_numbers=True)
                                        except:
                                            conclusionPercentage = None
                                        print(f"[SKY WAY] Progresso do Caminho do Céu: {conclusionPercentage}%")
                                        if conclusionPercentage is None:
                                            print("[SKY WAY] Não foi possível extrair o progresso do Caminho do Céu. Assumindo ZERO.")
                                            conclusionPercentage = 0
                                        else:
                                            conclusionPercentage = int(conclusionPercentage)
                                        if conclusionPercentage>=95 and not totalyCompleted:
                                            print("[SKY WAY] Chegou a 95% de conclusão, encerrando este Caminho")
                                            break
                                        else:
                                            buttonPlace=find(r"legend_bot\images\sky_way\inWayIndicator.png", confidence=0.8, region=BOTTOM_RIGHT)
                                            click(r"legend_bot\images\sky_way\searchWayButton.png", region=buttonPlace, confidence=0.8)
                                            if wait(r"legend_bot\images\sky_way\combatIndicator.png", confidence=0.8, timeout=30, region=TOP_RIGHT):
                                                print("[SKY WAY] Combate iniciado, aguardando conclusão...")
                                                wait_until_disappear(r"legend_bot\images\sky_way\combatIndicator.png", timeout=500, region=TOP_RIGHT)
                                                print("[SKY WAY] Combate concluído, continuando o Caminho do Céu...")
                                            else:
                                                print("[SKY WAY] Não houve combate, continuando o Caminho do Céu...")
                                        if exists(r"legend_bot\images\sky_way\skyWayCloseButton.png", confidence=0.8, region=FULL_SCREEN):
                                            click(r"legend_bot\images\sky_way\skyWayCloseButton.png", region=FULL_SCREEN, confidence=0.8)
                                            print("[SKY WAY] Janela fechada.")
                                        if not exists(r"legend_bot\images\sky_way\manaPoolEmpty.png", confidence=0.98, region=BOTTOM_BAR):
                                            print("não existe manaPool vazia")
                                            engine=True
                                        else:
                                            print("existe manaPool vazia")
                                            engine=False
                                            break
                                    click(r"legend_bot\images\sky_way\returnButton.png", region=buttonPlace, confidence=0.8)
                                    wait_time(2)
                            else:
                                i+=1
                                print(f"[SKY WAY] Desafio, tentando o próximo: {i+1}")
                        click(r"legend_bot\images\sky_way\skyWayExitButton.png", region=BOTTOM_RIGHT, confidence=0.8)
                        return True
                    else:
                        print("[SKY WAY] Não foi possível abrir a janela do Caminho do Céu.")
                        return False
                else:
                    print("[SKY WAY] Não foi possível encontrar o indicador do Caminho do Céu.")
                    return False
