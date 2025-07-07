from control import init_control, wait_if_paused
import time
from utils.screenVision import find, exists
from utils.actions import click, hover, scroll
init_control()

try:
    if exists("legend_bot/images/imagemTesteWait1.png"):
        print(">> A imagem da loja está visível!")
        click("legend_bot/images/imagemTesteWait1.png")

    pos = find("legend_bot/images/imagemTesteWait1.png")
    if pos:
        print(f">> Imagem da torre detectada em {pos}")


except KeyboardInterrupt:
    print("Bot finalizado com segurança.")