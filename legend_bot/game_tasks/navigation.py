from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import go_to_Interface
from utils.screenVision import exists, wait, find, find_all
from utils.actions import wait_time, click, click_position
from utils.regions import *
from datetime import timedelta

class Navigation(RepeatableTask):
    def __init__(self):
        super().__init__()
        self.interval = timedelta(minutes=80)
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 7

    def _run_task(self):
        """
        Implementa a lógica para coletar XP farm
        """
        print("Coletando Navegação...")
        go_to_Interface("castle") 
        if exists(r"legend_bot\images\navigation\interfaceButton.png", confidence=0.8, region=FULL_SCREEN) and self.running:
            click(r"legend_bot\images\navigation\interfaceButton.png", confidence=0.8, region=FULL_SCREEN)
            if (wait(r"legend_bot\images\navigation\windowBar.png", timeout=60, confidence=0.8, region=TOP_BAR) and self.running):
                residenceWindow_region=find(r"legend_bot\images\navigation\windowBar.png", confidence=0.8, region=TOP_BAR)
                if click(r"legend_bot\images\navigation\navigationButton.png", confidence=0.8, region=TOP_BAR):
                    if wait(r"legend_bot\images\navigation\navigationWindowBar.png",confidence=0.8, timeout=30, region=TOP_BAR):
                        navigation_region=find(r"legend_bot\images\navigation\navigationWindowBar.png",confidence=0.8, region=TOP_BAR)
                        if click(r"legend_bot\images\navigation\portButton.png", confidence=0.8, region=TOP_BAR):
                            if wait(r"legend_bot\images\navigation\portWindowBar.png",confidence=0.8, timeout=30, region=TOP_BAR):
                                port_location=find(r"legend_bot\images\navigation\portWindowBar.png",confidence=0.8, region=TOP_BAR)
                                if click(r"legend_bot\images\navigation\exchangeButton.png", confidence=0.8, region=port_location):
                                    if wait(r"legend_bot\images\navigation\materialSelection.png", confidence=0.8, timeout=10):
                                        if exists(r"legend_bot\images\navigation\menu.png", confidence=0.95, region=BOTTOM_BAR):
                                            menu_location=find(r"legend_bot\images\navigation\menu.png", confidence=0.9, region=BOTTOM_BAR)
                                            options = find_all(r"legend_bot\images\navigation\materialSelection.png", confidence=0.8)
                                            for option in options:
                                                click(r"legend_bot\images\navigation\acceptButton.png", region=option, confidence=0.8)
                                                wait_time(3)
                                            wait_time(7)

                                            possibleGain=0
                                            for option in options:
                                                if exists(r"legend_bot\images\navigation\acceptedIndicator.png", region=option, confidence=0.9):
                                                    possibleGain+=1

                                            if possibleGain>=2:
                                                if click(r"legend_bot\images\navigation\exchangeConfirmerButton.png", region=menu_location, confidence=0.8):
                                                    if wait(r"legend_bot\images\navigation\shipWindowBar.png", confidence=0.8, region=TOP_BAR):
                                                        ship = click(r"legend_bot\images\navigation\ship.png", confidence=0.92, region=FULL_SCREEN)
                                                        if not ship:
                                                            ship = click(r"legend_bot\images\navigation\ship2.png", confidence=0.92, region=FULL_SCREEN)
                                                        if ship:
                                                            wait_time(1)
                                                            if click(r"legend_bot\images\navigation\confirmShipButton.png", region=FULL_SCREEN , confidence=0.9):
                                                                wait_time(2)
                                                                print("[Navegação] Troca realizada com sucesso")
                                                            else:
                                                                click(r"legend_bot\images\navigation\cancelShipButton.png", region=FULL_SCREEN, confidence=0.9)
                                                                wait_time(2)
                                                        else:
                                                            print("[Navegação] Erro, nenhum navio detectado")
                                                            return False
                                                    else:
                                                        print("[Navegação] Menu de navios não foi aberto")
                                                        return False
                                                else:
                                                    print("[Navegação] Botão para navegar após escolha de itens não detectado")
                                                    return False
                                            else:
                                                if click(r"legend_bot\images\navigation\declineButton.png", confidence=0.9, region=menu_location):
                                                    wait_time(3)
                                                    if exists(r"legend_bot\images\navigation\confirmDeclineWindow.png", region=FULL_SCREEN, confidence=0.8):
                                                        confirmer_place=find(r"legend_bot\images\navigation\confirmDeclineWindow.png", region=FULL_SCREEN, confidence=0.8)
                                                        if click(r"legend_bot\images\navigation\confirmDeclineButton.png", region=confirmer_place, confidence=0.9):
                                                            wait_time(2)
                                                            click(r"legend_bot\images\navigation\portExitButton.png", confidence=0.9, region=port_location)
                                                            wait_time(2)

                                        elif exists(r"legend_bot\images\navigation\cantNavigateNowIndicator.png", confidence=0.93, region=BOTTOM_BAR):
                                            print("[Navegação] Porto indisponivel no momento")
                                            click(r"legend_bot\images\navigation\portExitButton.png", confidence=0.9, region=port_location)
                                            wait_time(2)
                                        else:
                                            print("[Navegação] Deu ruim irmão, não sei oq rolou")
                                            return False
                                    else:
                                        print("[Navegação] Não mostrou as negociações disponíveis")
                                        return False
                                else:
                                    print("[Navegação] Botão para selecionar trocas não encontrado")
                                    return False
                            else:
                                print("[Navegação] Interface do porto não abriu")
                                return False
                        else:
                            print("[Navegação] Porto não encontrado para clicar")
                            return False
                        click(r"legend_bot\images\navigation\residenceExitButton.png",region=navigation_region, confidence=0.9)
                        wait_time(3)
                    else:
                        print("[Navegação] Navegação não abriu")
                        return False
                else:
                    print("[Navegação] Botão de navegação nã encontrado na área da residencia")
                    return False
                click(r"legend_bot\images\navigation\residenceExitButton.png",region=residenceWindow_region, confidence=0.9)
                wait_time(3)
            else:
                print("[Navegação] Janela não encontrada.")
                return False
        else:
            print("[Navegação] Botão de farm não encontrado na região do castelo.")
            return False