from core.control import STOP, ERROR, PAUSED, pause, resume
from utils.general_use import prepare_window, move_mouse_outside_screen
import time, pyautogui, datetime
from datetime import datetime, timedelta
from utils.screenVision import master_exists, master_find, master_wait, master_wait_until_disappear
from utils.actions import master_click
from utils.regions import *

class TaskManager:
    def __init__(self, dailyTasks, fixedTasks, repeatableTasks, max_retries=3):
        self.dailyTasks = dailyTasks
        self.fixedTasks = fixedTasks
        self.repeatableTasks = repeatableTasks
        self.tasks = dailyTasks + fixedTasks + repeatableTasks
        self.currentTask = None
        self.errorTasks = []  # lista de tuplas (task, retries)
        self.lastTaskType = "Daily"
        self.max_retries = max_retries
        self.lastReload = datetime.now()

    def executeTasks(self):
        while not STOP:
            if datetime.now() - self.lastReload > timedelta(hours=1):
                pause()
                print("[INFO] Recarregando bot...")
                if not self.reload():
                    print("[ERRO] Falha ao recarregar. Tentando novamente...")
                    continue
                else:
                    print("[INFO] Bot recarregado com sucesso.")
                    self.lastReload = datetime.now()
                    resume()
            if not ERROR and not PAUSED:
                runTask = self.determine_nextTask()
                if runTask:
                    self.currentTask = runTask
                    prepare_window()
                    print(f"[TAREFA] Executando: {runTask.__class__.__name__}")
                    success = runTask.run()
                    if not success:
                        self._handle_task_error(runTask)
                    self.currentTask = None
                else:
                    print("[TAREFA] Nenhuma tarefa elegível no momento.")
                    time.sleep(2)
            else:
                print("[INFO] Pausado ou em erro. Aguardando...")
                time.sleep(2)

    def _handle_task_error(self, task):
        for i, (t, count) in enumerate(self.errorTasks):
            if t == task:
                self.errorTasks[i] = (t, count + 1)
                return
        self.errorTasks.append((task, 1))

    def determine_nextTask(self):
        # 1. Tarefas de horário fixo têm prioridade
        fixed = self._get_runnable_task(self.fixedTasks)
        if fixed:
            return fixed

        # 2. Verifica se há tarefas elegíveis em cada grupo
        daily_task = self._get_runnable_task(self.dailyTasks)
        repeatable_task = self._get_runnable_task(self.repeatableTasks)

        # 3. Alternância entre tipos, mas prioriza a disponível
        if self.lastTaskType == "Daily":
            if repeatable_task:
                self.lastTaskType = "Repeatable"
                return repeatable_task
            elif daily_task:
                # Continua com Daily, já que Repeatable não está disponível
                return daily_task
        elif self.lastTaskType == "Repeatable":
            if daily_task:
                self.lastTaskType = "Daily"
                return daily_task
            elif repeatable_task:
                return repeatable_task

        # 4. Se nenhuma das anteriores, reexecutar tarefas com erro
        if self.errorTasks:
            task, retry_count = self.errorTasks.pop(0)
            if retry_count < self.max_retries:
                self.errorTasks.append((task, retry_count))
                print(f"[TAREFA] Reexecutando após erro: {task.__class__.__name__} (tentativa {retry_count + 1})")
                return task
            else:
                print(f"[ERRO] {task.__class__.__name__} excedeu número máximo de tentativas.")

        return None
    
    def _get_runnable_task(self, task_list):
        # Ordena as tasks por prioridade crescente
        sorted_tasks = sorted(task_list, key=lambda task: getattr(task, "priority", 5))  # prioridade padrão = 5
        for task in sorted_tasks:
            if task.should_run():
                print(f"[TAREFA] {task.__class__.__name__} deve rodar agora (prioridade {task.priority})")
                return task
        return None
    
    def reload():
        pyautogui.press('esc')
        time.sleep(1)
        move_mouse_outside_screen()
        time.sleep(3)
        reconected=False
        retrys = 0
        while not reconected:
            print(f"[RECOVERY] Tentativa de reconexão {retrys}")
            menubar=master_find(r"legend_bot\images\recovery\menuBar.png", confidence=0.7, region=TOP_RIGHT)
            if menubar:
                master_click(r"legend_bot\images\recovery\refreshButton.png", region=menubar, confidence=0.8)
                time.sleep(2)
            time.sleep(1)
            move_mouse_outside_screen()
            time.sleep(3)
            
            if master_wait_until_disappear(r"legend_bot\images\recovery\disconectedIndicator.png", confidence=0.8, region=FULL_SCREEN, timeout=30):
                print("[RECOVERY] Indicador sumiu")
                if master_wait(r"legend_bot\images\recovery\preChargingWindow.png", timeout=90, confidence=0.8, region=FULL_SCREEN):
                    if master_wait(r"legend_bot\images\recovery\chargingWindow.png", timeout=120, confidence=0.8, region=FULL_SCREEN):
                        if master_wait_until_disappear(r"legend_bot\images\recovery\chargingWindow.png", timeout=180, confidence=0.8, region=FULL_SCREEN):
                            print("[RECOVERY] tela de carregamento sumiu")
                            count=0
                            while count<5 and not master_exists(r"legend_bot\images\recovery\inGameIndicator2.png", confidence=0.7, region=BOTTOM_LEFT, debug=True):
                                print(f"[RECOVERY] TEsperenado confirmação {count}")
                                time.sleep(24)
                                count+=1
                            if master_exists(r"legend_bot\images\recovery\inGameIndicator2.png", confidence=0.7, region=BOTTOM_LEFT):
                                if master_exists(r"legend_bot\images\recovery\castleButton.png", confidence=0.8,  region=TOP_RIGHT):
                                    master_click(r"legend_bot\images\recovery\castleButton.png", confidence=0.8, region=TOP_RIGHT)
                                    if master_wait(r"legend_bot\images\recovery\skyButton.png", timeout=60, confidence=0.8,  region=TOP_RIGHT):
                                        reconected = True
                                        print("[RECOVERY] Reconexão sucedida")
                    else:
                        print("Não entrou na tela de carregamento")
                        time.sleep(90)
                else:
                    print("2")
            else:
                print("1")
            retrys+=1
        if reconected:
            return True
        else:
            return False
