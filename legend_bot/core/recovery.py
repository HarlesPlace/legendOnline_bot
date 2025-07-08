import time, threading
from utils.screenVision import exists
from utils.actions import click
from core.control import happend_error, error_solved
from utils.window import active_game, open_game

# Número máximo de tentativas para recuperar
MAX_TENTATIVAS = 3
INTERVALO_CHECAGEM = 10  # segundos

def monitor_errors():
    tentativas = 0
    print("[RECOVERY] Monitoramento de falhas iniciado.")

    while True:
        # 1. Verifica se o jogo está fechado
        if not active_game():
            print("[RECOVERY] Jogo não está ativo. Tentando abrir...")
            happend_error()
            open_game()
            tentativas += 1
            time.sleep(15)
            continue

        # 2. Reconectar (tela de erro)
        if exists("legend_bot/imagens/reconectar.png"):
            print("[RECOVERY] Reconectando...")
            happend_error()
            click("legend_bot/imagens/reconectar.png")
            tentativas += 1
            time.sleep(10)
            continue

        # 3. Botão Jogar na tela de login
        if exists("legend_bot/imagens/botao_jogar.png"):
            print("[RECOVERY] Voltando ao jogo pela tela de login...")
            click("legend_bot/imagens/botao_jogar.png")
            tentativas += 1
            time.sleep(10)
            continue

        # 4. Se tudo estiver ok, resetamos tentativas
        if tentativas > 0:
            print("[RECOVERY] Jogo recuperado com sucesso.")
        tentativas = 0

        time.sleep(INTERVALO_CHECAGEM)

        # 5. Falha definitiva
        if tentativas >= MAX_TENTATIVAS:
            print("[RECOVERY] Falha crítica. Não foi possível recuperar o jogo.")
            #registrar_erro()
            break

def init_errorMonitor():
    listener = threading.Thread(target = monitor_errors, daemon = True)
    listener.start()