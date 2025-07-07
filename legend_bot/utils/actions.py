import pyautogui
import time
from utils.screenVision import wait

def hover(image_path, timeout=10, confidence=0.8):
    """
    Move o mouse até o centro da imagem detectada na tela.
    """
    position = wait(image_path, timeout=timeout, confidence=confidence,debug=False)
    if position:
        pyautogui.moveTo(position[0], position[1], duration=0.3)
        print(f"[INFO] Mouse movido até {position}")
        return True
    print("[ERRO] Imagem não encontrada para hover.")
    return False

def click(image_path, timeout=10, confidence=0.8):
    """
    Clica no centro da imagem detectada na tela.
    """
    if hover(image_path, timeout=timeout, confidence=confidence):
        pyautogui.click()
        print("[INFO] Clique executado.")
        return True
    print("[ERRO] Não foi possível clicar (imagem não encontrada).")
    return False

def type_text(text, BeforeImage_path = None, AfterImage_path=None, timeout=10, confidence=0.8, press_enter=False, clear_first=False):
    """
    Digita o texto fornecido. Se image_path for dado, clica na área antes de digitar.
    
    Parâmetros:
    - text: Texto a ser digitado
    - BeforeImage_path: Imagem da caixa de texto para clicar (opcional)
    - AfterImage_path: Imagem para clicar após digitar (opcional)
    - timeout: Tempo máximo para esperar a imagem (se fornecida)
    - confidence: Similaridade mínima (se usar imagem)
    - press_enter: Pressiona Enter após digitar?
    - clear_first: Pressiona Ctrl+A + Delete antes de digitar?
    """
    if BeforeImage_path:
        if not click(BeforeImage_path, timeout=timeout, confidence=confidence):
            print("[ERRO] Caixa de texto não encontrada para digitar.")
            return False
        time.sleep(0.2)  # Pequeno delay após clicar

    if clear_first:
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')

    pyautogui.write(text, interval=0.05)

    if AfterImage_path:
        if not click(AfterImage_path, timeout=timeout, confidence=confidence):
            print("[ERRO] Caixa de texto não encontrada para digitar.")
            return False
        time.sleep(0.2)  # Pequeno delay após clicar
        
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