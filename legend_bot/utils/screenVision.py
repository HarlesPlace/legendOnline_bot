import cv2
import numpy as np
import pyautogui
import time
from utils.highlight import highlight_area

def wait(image_path, timeout=10, confidence=0.8, debug=True):
    """
    Espera até que uma imagem apareça na tela ou o tempo esgote.
    Retorna o centro (x, y) da imagem encontrada ou None.
    """
    from core.control import wait_if_paused

    start_time = time.time()
    total_pause_time = 0
    while True:
        pause_start = time.time()
        wait_if_paused()
        pause_end = time.time()
        total_pause_time += pause_end - pause_start

        elapsed = time.time() - start_time - total_pause_time

        if debug:
            print(f"[DEBUG] Tempo de espera: {elapsed:.2f}s / Tempo limite: {timeout}s")

        if elapsed > timeout:
            print("[AVISO] Imagem não encontrada no tempo limite.")
            return None
        
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        template = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if template is None:
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if debug:
            print(f"[DEBUG] Similaridade: {max_val:.3f}")

        if max_val >= confidence:
            top_left = max_loc
            h, w = template.shape[:2]
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            
            if debug:
                highlight_area(top_left[0], top_left[1], w, h)

            print(f"[INFO] Imagem encontrada em ({center_x}, {center_y})")
            return (center_x, center_y)

        time.sleep(1)


def find(image_path, confidence=0.8, debug=True):
    """
    Procura uma imagem na tela neste momento.
    Retorna o centro (x, y) da imagem se encontrada, ou None.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if debug:
        print(f"[DEBUG] Similaridade: {max_val:.3f}")

    if max_val >= confidence:
        top_left = max_loc
        h, w = template.shape[:2]
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2

        if debug:
            highlight_area(top_left[0], top_left[1], w, h)

        return (center_x, center_y)

    return None

def exists(image_path, confidence=0.8, debug=False):
    """
    Verifica se uma imagem está presente na tela.
    Retorna True se encontrada, False caso contrário.
    """
    return find(image_path, confidence=confidence, debug=debug) is not None

def list_all(image_path, confidence=0.8, debug=True, min_distance=10):
    """
    Encontra todas as ocorrências da imagem na tela.
    Retorna uma lista com as posições (x, y) centrais encontradas.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    h, w = template.shape[:2]

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    y_coords, x_coords = np.where(result >= confidence)

    positions = []
    for (x, y) in zip(x_coords, y_coords):
        center_x = x + w // 2
        center_y = y + h // 2

        # Verifica se já existe um ponto próximo
        is_duplicate = any(
            abs(center_x - px) < min_distance and abs(center_y - py) < min_distance
            for px, py in positions
        )
        if not is_duplicate:
            positions.append((center_x, center_y))
            if debug:
                highlight_area(x, y, w, h)

    if debug:
        print(f"[INFO] {len(positions)} ocorrência(s) encontradas.")

    return positions
