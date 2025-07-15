from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import move_mouse_outside_screen, find_in_eventBar
from utils.screenVision import exists, wait, find
from utils.actions import wait_time, click
from utils.regions import *

class CollectOnlinePacket(RepeatableTask):
    def _run_task(self):
        """
        Implementa a lógica para coletar os pacotes de tempo online.
        """
        print("Coletando pacote online...")
        find_in_eventBar(r"legend_bot\images\online_packet_getter\onlinePacket.png")
        if exists(r"legend_bot\images\online_packet_getter\onlinePacket.png", confidence=0.85, region= TOP_BAR):
            click(r"legend_bot\images\online_packet_getter\onlinePacket.png", confidence=0.85, region= TOP_BAR)
            if wait(r"legend_bot\images\online_packet_getter\windowBar.png", confidence=0.85, region=TOP_BAR, timeout=60):
                if exists(r"legend_bot\images\online_packet_getter\colectButton.png", confidence=0.98, region=CENTER):
                    click(r"legend_bot\images\online_packet_getter\colectButton.png", confidence=0.98, region=CENTER)
                    wait_time(3)
                windowbarRegion = find(r"legend_bot\images\online_packet_getter\windowBar.png", confidence=0.85, region=TOP_BAR)
                click(r"legend_bot\images\online_packet_getter\packetOnlineExitButton.png", region=windowbarRegion, confidence=0.8)
                return True
            else: 
                print("[Pacote online] Janela não detectada")
                return False
        else:
            print("[Pacote online] Não detectado botão para a interface")
            return False