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

continuosTasks_list = [CollectOnlinePacket(), CollectSummer(), DemonCountry(), GetTattoo(),
                       Navigation(), PlantCrops(),
                       XPfarmColector()]
fixedTimeTasks_list = []
dailyTimeTasks_list = [ArenaPET(), GuardSearch(), SkyWay(),
                       SurroundingsSearch(), MainJudgment()]

def main():
    init_control()
    init_errorMonitor()
    bot = TaskManager(dailyTimeTasks_list, fixedTimeTasks_list,
                      continuosTasks_list, max_retries=4)
    bot.executeTasks()

if __name__ == "__main__":
    main()
