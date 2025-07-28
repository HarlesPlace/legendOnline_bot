from core.repeatable_task import RepeatableTask

from utils.general_use import open_map, by_map_go_to, sort_screen_matches
from utils.screenVision import exists, wait, find, find_all
from utils.actions import wait_time, click, click_position, type_text
from utils.regions import *
from datetime import timedelta

class DemonCountry(RepeatableTask):
    def __init__(self):
        super().__init__()
        self.interval = timedelta(minutes=120)
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 5 

    def _run_task(self):
        """
        Implementa a lógica para coletar continente do demônio
        """
        print("Coletando Continente do Demônio...")
        if open_map():
            if by_map_go_to("ContinenteDemonios"):
                if wait(r"legend_bot\images\demon_country\interfaceIndicator.png", timeout=90, region=FULL_SCREEN, confidence=0.8):
                    demonCountry_region=find(r"legend_bot\images\demon_country\interfaceIndicator.png", region=FULL_SCREEN, confidence=0.8)
                    click(r"legend_bot\images\demon_country\demonCountryButton.png", region= demonCountry_region, confidence=0.8)
                    if wait(r"legend_bot\images\demon_country\windowBar.png", timeout=30, region=TOP_BAR,confidence=0.8):
                        demonWindowBar_region=find(r"legend_bot\images\demon_country\windowBar.png", region=TOP_BAR, confidence=0.8)
                        godFragment=r"legend_bot\images\demon_country\godFragment.png"
                        equipamentFragment=r"legend_bot\images\demon_country\equipamentFragment.png"
                        larimarFragment=r"legend_bot\images\demon_country\larimarFragment.png"
                        engine=True
                        prices=[godFragment,equipamentFragment,larimarFragment]
                        for price in prices:
                            if (not engine) and (self.running):
                                break
                            if click(r"legend_bot\images\demon_country\firstRaidButton.png", confidence=0.95, region=BOTTOM_LEFT):
                                if wait(r"legend_bot\images\demon_country\inRaidIndicator.png", region=RIGHT_SIDE, confidence=0.8, timeout=15):
                                    inRaid_region=find(r"legend_bot\images\demon_country\inRaidIndicator.png", region=RIGHT_SIDE, confidence=0.8)
                                    nextRaid=True
                                    count=0
                                    while nextRaid and self.running and count<33:
                                        print(f"[Continente do demônio] Entrou na Raid: {count}")
                                        if not exists(price, region=TOP_BAR, confidence=0.75):
                                            print("[Continente do demônio] Fragmento desejado não encontrado")
                                            click(r"legend_bot\images\demon_country\nextRaidButton.png", region=inRaid_region, confidence=0.8)
                                            count+=1
                                            wait_time(3)
                                            if not exists(r"legend_bot\images\demon_country\bossButton.png", confidence=0.95, region=FULL_SCREEN):
                                                print("[Continente do demônio] Raid sem Boss disponível")
                                                nextRaid=False
                                        else:
                                            print("[Continente do demônio] Fragmento desejado encontrado")
                                            if not exists(r"legend_bot\images\demon_country\bossButton.png", confidence=0.95, region=FULL_SCREEN):
                                                nextRaid=False
                                                print("[Continente do Demônio] Fragmento desejado detectado, porém chefão não foi vencido ainda")
                                                break
                                            bosses=sort_screen_matches(find_all(r"legend_bot\images\demon_country\bossButton.png", confidence=0.95), axis='w')
                                            fightBossesInRaid=True
                                            for boss in bosses:
                                                if (not fightBossesInRaid) or (not self.running):
                                                    break
                                                if click_position(boss):
                                                    if wait(r"legend_bot\images\demon_country\inBossIndicator.png", confidence=0.8, region=FULL_SCREEN, timeout=15):
                                                        inBossMenu_region=find(r"legend_bot\images\demon_country\inBossIndicator.png", confidence=0.8, region=FULL_SCREEN)
                                                        if exists(r"legend_bot\images\demon_country\lastBossIndicator.png", region=BOTTOM_BAR, confidence=0.95):
                                                            print("[Continente do demônio] Chegou a última boss não vencido manualmente")
                                                            fightBossesInRaid=False
                                                            nextRaid=False
                                                        elif exists(r"legend_bot\images\demon_country\alredyDoneIndicator.png", confidence=0.95, region=BOTTOM_BAR):
                                                            print("[Continente do demônio] Boss já derrotado, indo para o proximo")
                                                            pass
                                                        elif exists(r"legend_bot\images\demon_country\normalInBossMenuBar.png", confidence=0.95, region=BOTTOM_BAR):
                                                            print("[Continente do demônio] Desafiar boss")
                                                            menuBar_region=find(r"legend_bot\images\demon_country\normalInBossMenuBar.png", confidence=0.95, region=BOTTOM_BAR)
                                                            if click(r"legend_bot\images\demon_country\botButton.png", confidence=0.95, region=menuBar_region):
                                                                if wait(r"legend_bot\images\demon_country\botWindowBar.png", confidence=0.8, region=FULL_SCREEN):
                                                                    botwindow_region=find(r"legend_bot\images\demon_country\botWindowBar.png", confidence=0.8, region=FULL_SCREEN)
                                                                    if type_text("3",BeforeImage_path=r"legend_bot\images\demon_country\botTypeBox.png", 
                                                                                 AfterImage_path=r"legend_bot\images\demon_country\playBotButton.png", confidence=0.9):
                                                                        wait_time(5)
                                                                        if exists(r"legend_bot\images\demon_country\outOfEnergyIndicator.png", confidence=0.8, region=FULL_SCREEN):
                                                                            print("[Continente do demônio] Energia acabou, finalizando por hora")
                                                                            aware_region=find(r"legend_bot\images\demon_country\outOfEnergyIndicator.png", confidence=0.8, region=FULL_SCREEN)
                                                                            fightBossesInRaid=False
                                                                            nextRaid=False
                                                                            engine=False
                                                                            click(r"legend_bot\images\demon_country\cancelButton.png", region=aware_region, confidence=0.8)
                                                                            wait_time(2)
                                                                            click(r"legend_bot\images\demon_country\inBotExitButton.png", region=botwindow_region, confidence=0.8)
                                                                            wait_time(2)
                                                                        elif exists(r"legend_bot\images\demon_country\botOperatingMenu.png", region=FULL_SCREEN, confidence=0.8):
                                                                            botMenu_region=find(r"legend_bot\images\demon_country\botOperatingMenu.png", region=FULL_SCREEN, confidence=0.8)
                                                                            click(r"legend_bot\images\demon_country\accelerateBotButton.png", region=botMenu_region, confidence=0.8)
                                                                            wait_time(2)
                                                                            if wait(r"legend_bot\images\demon_country\botEndIndicator.png", timeout=200, confidence=0.8, region=FULL_SCREEN):
                                                                                click(r"legend_bot\images\demon_country\inBotExitButton.png", region=botwindow_region, confidence=0.8)
                                                                                wait_time(2)
                                                                            else:
                                                                                click(r"legend_bot\images\demon_country\concludeBotButton.png", region=botMenu_region, confidence=0.8)
                                                                                wait_time(2)
                                                        else:
                                                            print("[Continente do Demonio] não foi possível definir o Boss")
                                                        click(r"legend_bot\images\demon_country\inBossExitButton.png",region=inBossMenu_region, confidence=0.8)
                                                        wait_time(2)
                                                    else:
                                                        print("[Continente Demônio] Janela de Boss não abriu")
                                                        return False
                                                else:
                                                    print("[Continente Demônio] Impossível clicar em um boss")
                                                    return False
                                            if nextRaid:
                                                click(r"legend_bot\images\demon_country\nextRaidButton.png", region=inRaid_region, confidence=0.8)
                                                count+=1
                                                wait_time(2)
                                    click(r"legend_bot\images\demon_country\inRaidExitButton.png", region=inRaid_region, confidence=0.8)
                                    wait_time(2)
                                else:
                                    print("[Continente Demônio] Raid não abriu")
                                    return False
                            else:
                                print("[Continente Demônio] Botão de 1ºraide não encontrado")
                                return False
                        print("aaaaaaaaaaaaaaaaaaa")            
                        click(r"legend_bot\images\demon_country\demonCountryWindowBarEx" \
                        "itButton.png", region=demonWindowBar_region, confidence=0.8)
                        wait_time(2)
                        return True
                    else:
                        print("[Continente Demônio] Não entrou no continente do demonio")
                        return False 
                else:
                    print("[Continente Demônio] Interface não apareceu")
                    return False




