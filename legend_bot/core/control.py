import keyboard
import threading
import time
from functools import wraps

PAUSED = False
STOP = False
ERROR = False
DEBUG = False

def all_Ok():
    return (not PAUSED and not ERROR and not STOP)

def wait_until_all_ok(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        while not all_Ok():
            #if PAUSED:
            #    print("[BOT PAUSADO]")
            #if ERROR:
            #    print("[BOT EM ERRO]")
            time.sleep(0.5)

        return func(*args, **kwargs)
    return wrapper

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
    while (PAUSED or ERROR) and not STOP:
        #if PAUSED and ERROR:
        #    print("[BOT PAUSADO E COM ERRO]")
        #elif ERROR:
        #    print("[BOT COM ERRO]")
        #elif PAUSED:
        #    print("[BOT PAUSADO]")
        time.sleep(0.5)
    if STOP:
        raise KeyboardInterrupt("Execução encerrada.")
    
def happend_error():
    print(">> [Aconteceu um erro]")
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