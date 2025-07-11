from utils.screenVision import exists, wait, find
from utils.actions import click, wait_time
from utils.regions import *

def close_comunicates():
    """
    Fecha os comunicados que aparecem na tela
    """
    while True:
        if exists("legend_bot/images/close_comunicates/comunicatesLabel.png", confidence=0.8, debug=False, region=BOTTOM_RIGHT):
           click("legend_bot/images/close_comunicates/closeButtom.png", confidence=0.8, region=BOTTOM_RIGHT)
           wait_time(3)
        else:
            break

def maximizeGameWindow():
    """
    Maximiza a janela do jogo
    """
    if exists("legend_bot/images/maximize_Game_Window/notMaxWindowDetail.png", confidence=0.8, debug=False, region=TOP_RIGHT):
        click("legend_bot/images/maximize_Game_Window/maximizeButton.png", confidence=0.8, region=TOP_LEFT)
        wait_time(3)
    else:
        print("[INFO] Janela do jogo já está maximizada ou não foi possível encontrar o botão.")
    if exists("legend_bot/images/maximize_Game_Window/maximizePermissionRequest.png", confidence=0.8, debug=False, region=TOP_BAR):
        click("legend_bot/images/maximize_Game_Window/confirmMaximizeButton.png", confidence=0.8, region=TOP_BAR)
        wait_time(3)
    return True

def go_to_Interface(interface_name):
    """
    Navega para a interface do castelo
    """
    if interface_name == "castle":
        if exists("legend_bot/images/go_to_Interface/skyButton.png", confidence=0.8, debug=False, region=TOP_RIGHT):
            return True
        else:
            if exists("legend_bot/images/go_to_Interface/castleButton.png", confidence=0.8, debug=False, region=TOP_RIGHT):
                click("legend_bot/images/go_to_Interface/castleButton.png", confidence=0.8, region=TOP_RIGHT)
                wait("legend_bot/images/go_to_Interface/skyButton.png", timeout=60, confidence=0.8, debug=False, region=TOP_RIGHT)
            else:
                print("[ERRO] Botão do castelo não encontrado.")
                return False
    elif interface_name == "sky":
        if exists("legend_bot/images/go_to_Interface/castleButton.png", confidence=0.8, debug=False, region=TOP_RIGHT):
            return True
        else:
            if exists("legend_bot/images/go_to_Interface/skyButton.png", confidence=0.8, debug=False, region=TOP_RIGHT):
                click("legend_bot/images/go_to_Interface/skyButton.png", confidence=0.8, region=TOP_RIGHT)
                wait("legend_bot/images/go_to_Interface/castleButton.png", timeout=60, confidence=0.8, debug=False, region=TOP_RIGHT)
            else:
                print("[ERRO] Botão do reino do céu não encontrado.")
                return False
            
def prepare_window():
    """
    Prepara a janela do jogo para o bot
    """
    maximizeGameWindow()
    close_comunicates()
    if exists("legend_bot/images/prepare_window/eventsColapserButton.png", confidence=0.95, debug=False, region=TOP_RIGHT):
        click("legend_bot/images/prepare_window/eventsColapserButton.png", confidence=0.95, region=TOP_RIGHT)
        wait("legend_bot/images/prepare_window/eventsUncolapserButton.png", timeout=15, confidence=0.95, debug=False, region=TOP_RIGHT)
    if exists("legend_bot/images/prepare_window/chatColapseControl.png", confidence=0.95, debug=False, region=BOTTOM_LEFT):
        especificPlace=find("legend_bot/images/prepare_window/chatColapseControl.png", confidence=0.8, region=BOTTOM_LEFT, debug=False)
        print(f"[INFO] Especific place found: {especificPlace}")
        click("legend_bot/images/prepare_window/chatColapserButton.png", confidence=0.8, region=especificPlace)
        wait_time(3)
        click("legend_bot/images/prepare_window/chatColapserButton.png", confidence=0.8, region=especificPlace)
        wait_time(3)
    if exists("legend_bot/images/prepare_window/missionsColapserButton.png", confidence=0.95, debug=False, region=TOP_RIGHT):
        click("legend_bot/images/prepare_window/missionsColapserButton.png", confidence=0.95, region=TOP_RIGHT)
        wait_time(3)
