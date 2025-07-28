from core.repeatable_task import RepeatableTask
from datetime import datetime

from utils.general_use import go_to_Interface, find_in_eventBar
from utils.screenVision import exists, wait, find
from utils.actions import wait_time, click
from utils.regions import *
from datetime import timedelta

class CollectOnlinePacket(RepeatableTask):
    def __init__(self):
        super().__init__()
        self.interval = timedelta(minutes=30)
        self.blackout_hours = []
        self.allowed_weekdays = [0, 1, 2, 3, 4, 5, 6]
        self.priority = 0

    def _run_task(self):
        """
        Implementa a lógica para coletar os pacotes de tempo online.
        """
        print("Coletando pacote online...")
        go_to_Interface("castle")
        find_in_eventBar(r"legend_bot\images\online_packet_getter\onlinePacket.png")
        if exists(r"legend_bot\images\online_packet_getter\onlinePacket.png", confidence=0.85, region= TOP_BAR):
            click(r"legend_bot\images\online_packet_getter\onlinePacket.png", confidence=0.85, region= TOP_BAR)
            if wait(r"legend_bot\images\online_packet_getter\windowBar.png", confidence=0.85, region=TOP_BAR, timeout=60):
                if exists(r"legend_bot\images\online_packet_getter\colectButton.png", confidence=0.98, region=CENTER):
                    click(r"legend_bot\images\online_packet_getter\colectButton.png", confidence=0.98, region=CENTER)
                    wait_time(3)
                windowbarRegion = find(r"legend_bot\images\online_packet_getter\windowBar.png", confidence=0.85, region=TOP_BAR)
                click(r"legend_bot\images\online_packet_getter\packetOnlineExitButton.png", region=windowbarRegion, confidence=0.8)    
            else: 
                print("[Pacote online] Janela não detectada")
                return False
        else:
            print("[Pacote online] Não detectado botão para a interface")
            
        return True