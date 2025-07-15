from core.daily_task import DailyTask
from utils.general_use import open_map, by_map_go_to, move_mouse_outside_screen
from utils.screenVision import exists, wait, find, list_all, check_right, wait_until_disappear
from utils.actions import wait_time, click, click_position
from utils.regions import *
from utils.OCR import extract_text_right_of_image, extract_text_from_position

class ArenaPET(DailyTask):
    def _run_task(self):
        if open_map():
            if by_map_go_to("ArenaPET"):
                if wait(r"legend_bot\images\arena_PET\interfaceIndicator.png", confidence=0.8, timeout=30, region=FULL_SCREEN):
                    arenaPET_region = find(r"legend_bot\images\arena_PET\interfaceIndicator.png", confidence=0.8,region=FULL_SCREEN, debug=False)
                    click(r"legend_bot\images\arena_PET\arenaPETbutton.png", region=arenaPET_region, confidence=0.8)
                    if wait(r"legend_bot\images\arena_PET\windowBar.png", confidence=0.8, timeout=30, region=TOP_BAR):
                        mypower=int(extract_text_right_of_image(r"legend_bot\images\arena_PET\myPowerIndicator.png",confidence=0.8, width=140, invert=True, only_numbers=True))
                        print(f"[ARENA PET] Meu poder: {mypower}")
                        i=0
                        while i<10 and self.running:
                            allOpponentsLocations= list_all(r"legend_bot\images\arena_PET\enemyPowerIndicator.png", confidence=0.8)
                            j=len(allOpponentsLocations)
                            enemyPower=[]
                            chalengeButtonLocations = []
                            for k in range(j):
                                enemyPower.append(int(extract_text_from_position(allOpponentsLocations[k], offset=(30,-10,90,20), invert=True, only_numbers=True)))
                                chalengeButtonLocations.append(check_right(position=allOpponentsLocations[k], image_path= r"legend_bot\images\arena_PET\chalengeButton.png", 
                                                                           offset=(20, -70), region_size=(200, 100), confidence=0.8, debug=True))
                            print(f"[ARENA PET] Poder dos oponentes: {enemyPower}")
                            print(f"[ARENA PET] Botões de desafio encontrados: {chalengeButtonLocations}")
                            if len(enemyPower) > 0:
                                minPower = min(enemyPower)
                                minPowerIndex = enemyPower.index(minPower)
                                print(f"[ARENA PET] Desafiando oponente {minPowerIndex} com poder {minPower}.")
                                move_mouse_outside_screen()
                                click_position(chalengeButtonLocations[minPowerIndex])
                                wait_time(2)
                                if wait_until_disappear(r"legend_bot\images\arena_PET\windowBar.png", timeout=60, confidence=0.8, region=TOP_BAR):
                                    if wait(r"legend_bot\images\arena_PET\inBatleIndicator.png", confidence=0.8, timeout=60, region=TOP_BAR):
                                        print("[ARENA PET] Entrou em batalha.")
                                        if wait(r"legend_bot\images\arena_PET\windowBar.png", confidence=0.8, timeout=120, region=TOP_BAR):
                                            print("[ARENA PET] Batalha concluída. Retornou a tela da Arena PET.")
                                        else:
                                            print("[ARENA PET] Interface não encontrada após a batalha.")
                                            return False
                                    else:
                                        print("[ARENA PET] Tela de batalha não encontrada.")
                                        if exists(r"legend_bot\images\arena_PET\windowBar.png", region=TOP_BAR, confidence=0.8):
                                            print("[ARENA PET] Algo estranho ocorreu, mas Retornou à tela de desafio.")
                                        else:
                                            print("[ARENA PET] Algo deu errado, não retornou à tela de desafio.")
                                            return False
                                else:
                                    print("[ARENA PET] Não entrou em batalha.")
                                i += 1
                            else:
                                print("[ARENA PET] Nenhum oponente disponível.")
                        click(r"legend_bot\images\arena_PET\arenaPETexitButton.png", region=TOP_RIGHT, confidence=0.8)
                        wait_time(5)
                        return True
                    else:
                        print("Não foi possível encontrar a barra de janela da Arena PET.")
                        return False
                else:
                    print("Não foi possível encontrar o indicador da Arena PET.")
                    return False

