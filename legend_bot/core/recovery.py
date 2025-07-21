import time, threading
from utils.screenVision import exists, find, wait, wait_until_disappear
from utils.actions import click
from core.control import happend_error, STOP, error_solved
from utils.window import active_game, open_game
from utils.regions import *

# Número máximo de tentativas para recuperar
MAX_TENTATIVAS = 3
INTERVALO_CHECAGEM = 10  # segundos

def reconect():
    reconected=False
    retrys = 0
    while retrys<MAX_TENTATIVAS and not reconected:
        disconectionWarn = find(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.7, region=FULL_SCREEN)
        menubar=find(r"legend_bot\images\recovery\menuBar.png", confidence=0.7, region=TOP_RIGHT)
        if menubar:
            click(r"legend_bot\images\recovery\refreshButton.png", region=menubar, confidence=0.8)
            time.sleep(2)
        elif disconectionWarn:
            if click(r"legend_bot\images\recovery\confirmDisconectionButton.png", region=disconectionWarn, confidence=0.8):
                if wait(r"legend_bot\images\recovery\reloadIndicator.png", region=FULL_SCREEN, confidence=0.8, timeout=5):
                    reloadWarn=find(r"legend_bot\images\recovery\reloadIndicator.png", region=FULL_SCREEN, confidence=0.8)
                    click(r"legend_bot\images\recovery\reloadButton.png", region=reloadWarn, confidence=0.9)
        
        if wait_until_disappear(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.7, region=FULL_SCREEN, timeout=30):
            if wait(r"legend_bot\images\recovery\preChargingWindow.png", timeout=90, confidence=0.8, region=FULL_SCREEN):
                if wait(r"legend_bot\images\recovery\chargingWindow.png", timeout=120, confidence=0.8, region=FULL_SCREEN):
                    if wait_until_disappear(r"legend_bot\images\recovery\chargingWindow.png", timeout=180, confidence=0.8, region=FULL_SCREEN):
                        count=0
                        while count<5 and not exists(r"legend_bot\images\recovery\inGameIndicator2.png", confidence=0.75, region=BOTTOM_RIGHT):
                            time.sleep(24)
                            count+=1
                        if exists(r"legend_bot\images\recovery\inGameIndicator2.png", confidence=0.75, region=BOTTOM_RIGHT):
                            if exists(r"legend_bot\images\recovery\castleButton.png", confidence=0.8,  region=TOP_RIGHT):
                                click(r"legend_bot\images\recovery\castleButton.png", confidence=0.8, region=TOP_RIGHT)
                                if wait(r"legend_bot\images\recovery\skyButton.png", timeout=60, confidence=0.8,  region=TOP_RIGHT):
                                    reconected = True
                else:
                    print("Não entrou na tela de carregamento")
                    time.sleep(90)
        retrys+=1
    if reconected:
        return True
    else:
        return False

def monitor_errors():
    tentativas = 0
    print("[RECOVERY] Monitoramento de falhas iniciado.")
    while not STOP:
        if exists(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.65, region=FULL_SCREEN):
            print("[RECOVERY] Reconectando...")
            happend_error()
            reconected=reconect()
            if reconected:
                error_solved()
                continue
            else:
                tentativas += 1
    print("[RECOVERY] Encerrando monitoramento")

def init_errorMonitor():
    listener = threading.Thread(target = monitor_errors, daemon = True)
    listener.start()