import pyautogui
import time
from utils.screenVision import wait, find, list_all

def hover(image_path, confidence=0.8, region=None):
    """
    Move o mouse até o centro da imagem detectada na tela.
    """
    position = find(image_path, confidence=confidence, debug=False, region=region)
    if position:
        pyautogui.moveTo(position[0]+position[2]/2, position[1]+position[3]/2, duration=0.3)
        print(f"[INFO] Mouse movido até {position}")
        return True
    print("[ERRO] Imagem não encontrada para hover.")
    return False

def hover_position(position, duration=0.3):
    """
    Move o mouse até a posição (x, y) fornecida.

    Parâmetros:
    - position: tupla (x, y)
    - duration: tempo (em segundos) para o movimento do cursor
    """
    if position and len(position) == 2:
        x, y = map(int,position)
        pyautogui.moveTo(x, y, duration=duration)
        print(f"[INFO] Mouse movido até {position}")
        return True
    else:
        print("[ERRO] Posição inválida fornecida para hover.")
        return False
    
def click(image_path, confidence=0.8, region=None):
    """
    Clica no centro da imagem detectada na tela.
    """
    if hover(image_path, confidence=confidence, region=region):
        pyautogui.click()
        print("[INFO] Clique executado.")
        return True
    print("[ERRO] Não foi possível clicar (imagem não encontrada).")
    return False

def type_text(text, BeforeImage_path = None, AfterImage_path=None, confidence=0.8, press_enter=False, clear_first=False):
    """
    Digita o texto fornecido. Se image_path for dado, clica na área antes de digitar.
    
    Parâmetros:
    - text: Texto a ser digitado
    - BeforeImage_path: Imagem da caixa de texto para clicar (opcional)
    - AfterImage_path: Imagem para clicar após digitar (opcional)
    - confidence: Similaridade mínima (se usar imagem)
    - press_enter: Pressiona Enter após digitar?
    - clear_first: Pressiona Ctrl+A + Delete antes de digitar?
    """
    if BeforeImage_path:
        if not click(BeforeImage_path, confidence=confidence):
            print("[ERRO] Caixa de texto não encontrada para digitar. Antes")
            return False
        time.sleep(0.5)  # Pequeno delay após clicar

    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.3)
    if clear_first:
        pyautogui.press('delete')

    pyautogui.write(text, interval=0.05)

    if AfterImage_path:
        if not click(AfterImage_path, confidence=confidence):
            print("[ERRO] Caixa de texto não encontrada para digitar. Depois")
            return False
        time.sleep(0.5)  # Pequeno delay após clicar
        
    if press_enter:
        pyautogui.press('enter')

    print(f"[INFO] Texto digitado: '{text}'")
    return True

def scroll(direction='down', amount=1, step=100, position=None, delay=0.1):
    """
    Rola a tela na direção especificada.

    - direction: 'up', 'down', 'left', 'right'
    - amount: número de rolagens
    - step: intensidade (padrão 100 por rolagem)
    - position: tupla (x, y) para mover o mouse antes de rolar (opcional)
    - delay: tempo entre rolagens
    """
    if position:
        pyautogui.moveTo(position[0], position[1], duration=0.2)

    for _ in range(amount):
        if direction == 'up':
            pyautogui.scroll(step)
        elif direction == 'down':
            pyautogui.scroll(-step)
        elif direction == 'left':
            pyautogui.hscroll(-step)
        elif direction == 'right':
            pyautogui.hscroll(step)
        else:
            print(f"[ERRO] Direção inválida: {direction}")
            return False
        time.sleep(delay)

    print(f"[INFO] Scroll {direction} realizado {amount}x (step={step})")
    return True

def drag(from_image, to_image, timeout=10, confidence=0.8):
    """
    Arrasta o mouse do centro de from_image até o centro de to_image.

    - from_image: caminho da imagem onde começa o arrasto
    - to_image: caminho da imagem onde termina
    - timeout: tempo máximo para esperar as imagens
    - confidence: similaridade mínima para encontrar as imagens
    """
    start_pos = wait(from_image, timeout=timeout, confidence=confidence)
    if not start_pos:
        print("[ERRO] Imagem de origem não encontrada para drag.")
        return False

    end_pos = wait(to_image, timeout=timeout, confidence=confidence)
    if not end_pos:
        print("[ERRO] Imagem de destino não encontrada para drag.")
        return False

    pyautogui.moveTo(start_pos[0], start_pos[1], duration=0.3)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.moveTo(end_pos[0], end_pos[1], duration=0.5)
    pyautogui.mouseUp()

    print(f"[INFO] Arrasto realizado de {start_pos} até {end_pos}")
    return True

def wait_time(seconds):
    """
    Espera um número específico de segundos.
    
    - seconds: tempo em segundos para esperar
    """
    from core.control import wait_if_paused_or_error

    start_time = time.time()
    total_pause_time = 0
    while True:
        pause_start = time.time()
        wait_if_paused_or_error()
        pause_end = time.time()
        total_pause_time += pause_end - pause_start

        elapsed = time.time() - start_time - total_pause_time

        if elapsed > seconds:
            print("[AVISO] Tempo de espera cumprido.")
            return None
        
        time.sleep(seconds)

def click_all(image_path, confidence=0.8, delay_between=1, debug=True):
    """
    Clica em todas as ocorrências de uma imagem na tela, com pequeno intervalo entre os cliques.

    - image_path: caminho da imagem a encontrar
    - confidence: nível de confiança para correspondência
    - delay_between: tempo (em segundos) entre cliques
    - debug: ativa highlight e prints
    """
    positions = list_all(image_path, confidence=confidence, debug=debug)

    for pos in positions:
        click_position(pos)
        wait_time(delay_between)

    if debug:
        print(f"[INFO] {len(positions)} clique(s) realizados.")

def click_position(position):
    """
    Clica em uma posição fornecida.

    - position: tupla (x, y) ou (x, y, w, h)
    """
    if len(position) == 2:
        x, y = map(int, position)
    elif len(position) == 4:
        x, y, w, h = map(int, position)
        x += w // 2
        y += h // 2
    else:
        raise ValueError("A posição deve ser uma tupla com 2 ou 4 valores.")
    pyautogui.moveTo(x, y)
    pyautogui.click()
    return True