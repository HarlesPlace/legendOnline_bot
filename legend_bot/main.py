from control import init_control, wait_if_paused
import time

init_control()

try:
    for i in range(100):
        wait_if_paused()
        print(f"Executando passo {i}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Bot finalizado com segurança.")