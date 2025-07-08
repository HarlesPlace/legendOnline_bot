import pygetwindow as gw
import subprocess
import os

# Nome da janela do Legend Online (ajuste conforme seu sistema)
JANELA_TITULO = "Legend Online"

def active_game():
    janelas = gw.getWindowsWithTitle(JANELA_TITULO)
    return any(janela.isVisible for janela in janelas)

def open_game():
    caminho_exe = r"C:\Caminho\para\LegendOnline.exe"  # ⚠️ Ajuste isso!
    if os.path.exists(caminho_exe):
        subprocess.Popen(caminho_exe)
        print("[RECOVERY] Executando jogo.")
    else:
        print(f"[RECOVERY] Caminho inválido: {caminho_exe}")
