from core.control import init_control
from core.recovery import init_errorMonitor
from core.task_manager import TaskManager
from game_tasks.demonCountry import DemonCountry
from game_tasks.arenaPET import ArenaPET
from game_tasks.colectSummer import CollectSummer
from game_tasks.fishing import Fishing
from game_tasks.getTattoo import GetTattoo
from game_tasks.guardSearch import GuardSearch
from game_tasks.navigation import Navigation
from game_tasks.onlinePacketGeter import CollectOnlinePacket
from game_tasks.plantCrops import PlantCrops
from game_tasks.skyWay import SkyWay
from game_tasks.surroundingsSearch import SurroundingsSearch
from game_tasks.xpFarmColect import XPfarmColector
from game_tasks.mainJudgment import MainJudgment
from game_tasks.labirinth import Labirinth
from game_tasks.guildTreasure import GuildTreasure
from game_tasks.arena import Arena
from game_tasks.assassinationOfMidnight import AssassinationOfMidnight
from game_tasks.ecliptTemple import EcliptTemple

continuosTasks_list = [CollectOnlinePacket(), 
                       CollectSummer(), 
                       DemonCountry(), 
                       GetTattoo(),
                       Navigation(), 
                       PlantCrops(), 
                       XPfarmColector(), 
                       EcliptTemple()]

fixedTimeTasks_list = [Fishing(),
                       Arena(),
                       AssassinationOfMidnight()]

dailyTimeTasks_list = [ArenaPET(),
                       GuardSearch(),
                       SkyWay(),
                       SurroundingsSearch(),
                       MainJudgment(),
                       Labirinth()]

def main():
    init_control()
    init_errorMonitor()
    bot = TaskManager(dailyTimeTasks_list, fixedTimeTasks_list, continuosTasks_list)
    bot.executeTasks()

if __name__ == "__main__":
    main()
