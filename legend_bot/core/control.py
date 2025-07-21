import keyboard
import threading
import time

PAUSED = False
STOP = False
ERROR = False
DEBUG = False

def pause_or_continue():
    global PAUSED
    PAUSED = not PAUSED
    print(">> [PAUSA]" if PAUSED else ">> [RETOMADO]")

def finish():
    global STOP
    STOP = True
    print(">> [ENCERRANDO BOT...]")

def listen_keyboard():
    keyboard.add_hotkey('ctrl+alt+p', pause_or_continue)
    keyboard.add_hotkey('ctrl+alt+s', finish)
    print("[CONTROLES] Ctrl+Alt+P = Pausar/Retomar | Ctrl+Alt+S = Parar")
    keyboard.wait('ctrl+alt+s')  # mantém vivo até o fim

def init_control():
    listener = threading.Thread(target = listen_keyboard, daemon = True)
    listener.start()

def wait_if_paused_or_error():
    while (PAUSED and (not STOP) and (not ERROR)):
        print("[BOT PAUSADO]")
        time.sleep(0.5)
    if STOP:
        raise KeyboardInterrupt("Execução encerrada.")
    
def happend_error():
    global ERROR
    ERROR = True

def error_solved():
    global ERROR
    ERROR = False
    print(">> [ERRO RESOLVIDO] O bot pode continuar a execução.")
    if not PAUSED:
        print(">> [RETOMANDO EXECUÇÃO]")
    else:
        print(">> [BOT PAUSADO] Pressione Ctrl+Alt+P para retomar.")