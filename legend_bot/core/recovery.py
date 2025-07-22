import time, threading, pyautogui
from utils.screenVision import master_exists, master_find, master_wait, master_wait_until_disappear
from utils.actions import master_click
from core.control import happend_error, STOP, error_solved
from utils.window import active_game, open_game
from utils.regions import *
from utils.general_use import move_mouse_outside_screen

# Número máximo de tentativas para recuperar
MAX_TENTATIVAS = 3
INTERVALO_CHECAGEM = 10  # segundos

def reconect():
    pyautogui.press('esc')
    time.sleep(1)
    move_mouse_outside_screen()
    time.sleep(3)
    reconected=False
    retrys = 0
    while retrys<MAX_TENTATIVAS and not reconected:
        print(f"[RECOVERY] Tentativa de reconexão {retrys}")
        disconectionWarn = master_find(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.7, region=FULL_SCREEN)
        menubar=master_find(r"legend_bot\images\recovery\menuBar.png", confidence=0.7, region=TOP_RIGHT)
        if menubar:
            master_click(r"legend_bot\images\recovery\refreshButton.png", region=menubar, confidence=0.8)
            time.sleep(2)
        elif disconectionWarn:
            if master_click(r"legend_bot\images\recovery\confirmDisconectionButton.png", region=disconectionWarn, confidence=0.8):
                if master_wait(r"legend_bot\images\recovery\reloadIndicator.png", region=FULL_SCREEN, confidence=0.8, timeout=5):
                    reloadWarn=master_find(r"legend_bot\images\recovery\reloadIndicator.png", region=FULL_SCREEN, confidence=0.8)
                    master_click(r"legend_bot\images\recovery\reloadButton.png", region=reloadWarn, confidence=0.9)
        time.sleep(1)
        move_mouse_outside_screen()
        time.sleep(3)
        
        if master_wait_until_disappear(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.8, region=FULL_SCREEN, timeout=30):
            print("[RECOVERY] Indicador sumiu")
            if master_wait(r"legend_bot\images\recovery\preChargingWindow.png", timeout=90, confidence=0.8, region=FULL_SCREEN):
                if master_wait(r"legend_bot\images\recovery\chargingWindow.png", timeout=120, confidence=0.8, region=FULL_SCREEN):
                    if master_wait_until_disappear(r"legend_bot\images\recovery\chargingWindow.png", timeout=180, confidence=0.8, region=FULL_SCREEN):
                        print("[RECOVERY] tela de carregamento sumiu")
                        count=0
                        while count<5 and not master_exists(r"legend_bot\images\recovery\inGameIndicator2.png", confidence=0.7, region=BOTTOM_LEFT, debug=True):
                            print(f"[RECOVERY] TEsperenado confirmação {count}")
                            time.sleep(24)
                            count+=1
                        if master_exists(r"legend_bot\images\recovery\inGameIndicator2.png", confidence=0.7, region=BOTTOM_LEFT):
                            if master_exists(r"legend_bot\images\recovery\castleButton.png", confidence=0.8,  region=TOP_RIGHT):
                                master_click(r"legend_bot\images\recovery\castleButton.png", confidence=0.8, region=TOP_RIGHT)
                                if master_wait(r"legend_bot\images\recovery\skyButton.png", timeout=60, confidence=0.8,  region=TOP_RIGHT):
                                    reconected = True
                                    print("[RECOVERY] Reconexão sucedida")
                else:
                    print("Não entrou na tela de carregamento")
                    time.sleep(90)
            else:
                print("2")
        else:
            print("1")
        retrys+=1
    if reconected:
        return True
    else:
        return False

def monitor_errors():
    tentativas = 0
    print("[RECOVERY] Monitoramento de falhas iniciado.")
    while not STOP:
        if isDisconected():
            print("[RECOVERY] Reconectando...")
            happend_error()
            reconected=reconect()
            if reconected:
                error_solved()
                continue
            else:
                tentativas += 1
                print("[ERROR MONITORING] Falhou na reconexão")
    print("[RECOVERY] Encerrando monitoramento")

def init_errorMonitor():
    listener = threading.Thread(target = monitor_errors, daemon = True)
    listener.start()

def isDisconected():
    return master_exists(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.65, region=FULL_SCREEN)