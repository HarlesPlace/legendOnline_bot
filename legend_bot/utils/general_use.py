from utils.screenVision import exists, wait, find, wait_until_disappear
from utils.actions import click, wait_time, click_position
from utils.regions import *
from utils.mapsCoords import MAP_LOCATIONS
import pyautogui

pyautogui.FAILSAFE = False

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

    #se abriu algo por engano fecha
    if exists(r"legend_bot\images\maximize_Game_Window\closeButton.png", confidence=0.8, debug=False, region=TOP_RIGHT):
        click(r"legend_bot\images\maximize_Game_Window\closeButton.png", confidence=0.8, region=TOP_RIGHT)
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
                close_comunicates()
                return True
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
                close_comunicates()
                return True
            else:
                print("[ERRO] Botão do reino do céu não encontrado.")
                return False
    else:
        raise ValueError
            
def prepare_window():
    """
    Prepara a janela do jogo para o bot
    """
    maximizeGameWindow()
    closeMissionBar()
    close_comunicates()
    if exists("legend_bot/images/prepare_window/eventsColapserButton.png", confidence=0.95, debug=False, region=TOP_RIGHT):
        click("legend_bot/images/prepare_window/eventsColapserButton.png", confidence=0.95, region=TOP_RIGHT)
        wait("legend_bot/images/prepare_window/eventsUncolapserButton.png", timeout=15, confidence=0.95, debug=False, region=TOP_RIGHT)
    if exists("legend_bot/images/prepare_window/hidePlayersButton.png", confidence=0.95, debug=False, region=TOP_RIGHT):
        click("legend_bot/images/prepare_window/hidePlayersButton.png", confidence=0.95, region=TOP_RIGHT)
        wait_time(3)
    if exists("legend_bot/images/prepare_window/chatColapseControl.png", confidence=0.95, debug=False, region=BOTTOM_LEFT):
        especificPlace=find("legend_bot/images/prepare_window/chatColapseControl.png", confidence=0.8, region=BOTTOM_LEFT, debug=False)
        print(f"[INFO] Especific place found: {especificPlace}")
        click("legend_bot/images/prepare_window/chatColapserButton.png", confidence=0.8, region=especificPlace)
        wait_time(3)
        click("legend_bot/images/prepare_window/chatColapserButton.png", confidence=0.8, region=especificPlace)
        wait_time(3)

def closeMissionBar():
    if exists("legend_bot/images/prepare_window/missionsColapserButton.png", confidence=0.9, debug=False, region=TOP_RIGHT):
        click("legend_bot/images/prepare_window/missionsColapserButton.png", confidence=0.9, region=TOP_RIGHT)
        wait_time(3)

def move_mouse_outside_screen():
    """
    Move o cursor para fora da tela visível, evitando tooltips e interferência em OCR/imagem.
    """
    pyautogui.moveTo(0, 0)

def find_in_eventBar(image_path, confidence=0.9):
    """
    Encontra um elemento na barra de eventos.
    """
    if exists(r"legend_bot\images\find_in_eventBar\eventsUncolapserButton.png",confidence=0.8, debug=False, region=TOP_BAR):
        click(r"legend_bot\images\find_in_eventBar\eventsUncolapserButton.png",confidence=0.8, region=TOP_BAR)
        wait_time(5)
    move_mouse_outside_screen()
    if (not exists(image_path, confidence=confidence, debug=False, region=TOP_BAR)) and exists(r"legend_bot\images\find_in_eventBar\nextButton.png", confidence=0.9, debug=False, region=TOP_BAR):
        click(r"legend_bot\images\find_in_eventBar\nextButton.png", confidence=confidence, region=TOP_BAR, debug=False)
    elif ((not exists(image_path, confidence=confidence, debug=False, region=TOP_BAR)) and exists(r"legend_bot\images\find_in_eventBar\previewButton.png", confidence=0.9, debug=False, region=TOP_BAR)):
        click(r"legend_bot\images\find_in_eventBar\previewButton.png", confidence=confidence, region=TOP_BAR, debug=False)
    move_mouse_outside_screen()
    wait_time(6)
    if exists(image_path, confidence=confidence, debug=False, region=TOP_BAR):
        return True
    else:
        return False

def open_map():
    """
    Abre o mapa do jogo.
    """
    go_to_Interface("sky")
    mapbutton = find(r"legend_bot\images\by_map_go_to\mapButton.png", confidence=0.8, debug=False, region=BOTTOM_RIGHT)
    if not mapbutton:
        print("[ERRO] Botão do mapa não encontrado.")
        return False
    else:
        click_position(mapbutton)
        wait(r"legend_bot\images\by_map_go_to\map.png", timeout=20, confidence=0.8, debug=False, region=FULL_SCREEN)
        return True
    
def by_map_go_to(place_name):
    if place_name not in MAP_LOCATIONS:
        print(f"[ERRO] Local '{place_name}' não cadastrado no mapa.")
        return False

    map_location = find(r"legend_bot\images\by_map_go_to\map.png", confidence=0.8, debug=False)
    if not map_location:
        print("[ERRO] Mapa não encontrado na tela.")
        return False

    map_x, map_y, _, _ = map_location
    offset_x, offset_y = MAP_LOCATIONS[place_name]

    click_x = map_x + offset_x
    click_y = map_y + offset_y

    print(f"[INFO] Indo para '{place_name}' em ({click_x}, {click_y})")
    click_position((click_x, click_y))
    if wait_until_disappear(r"legend_bot\images\by_map_go_to\map.png", timeout=60, confidence=0.8, region=FULL_SCREEN):
        return True
    else:
        return False
 