import cv2
import numpy as np
import pyautogui
import time
import threading
from utils.highlight import highlight_area
from PIL import ImageGrab
from core.control import wait_if_paused_or_error, DEBUG, wait_until_all_ok

def master_wait(image_path, timeout=10, confidence=0.8, debug=DEBUG, region=None):
    """
    Espera até que uma imagem apareça na tela (ou região) ou até esgotar o tempo.

    - image_path: caminho da imagem a ser encontrada
    - timeout: tempo máximo em segundos
    - confidence: limiar mínimo de similaridade
    - debug: se True, exibe prints e destaque visual
    - region: tupla (x, y, w, h) opcional, define a área de busca

    Retorna:
    - (x, y): centro da imagem encontrada, ou None se não encontrada no tempo limite.
    """
    start_time = time.time()
    # Carrega o template uma vez fora do loop
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
    while True:
        elapsed = time.time() - start_time
        # Captura da tela ou região
        if region:
            rx, ry, rw, rh = region
            screenshot = ImageGrab.grab(bbox=(rx, ry, rx + rw, ry + rh))
        else:
            screenshot = pyautogui.screenshot()
            rx, ry = 0, 0  # caso seja tela cheia
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # Matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if debug:
            print(f"[DEBUG] Similaridade: {max_val:.3f}")
        if max_val >= confidence:
            top_left = (max_loc[0] + rx, max_loc[1] + ry)
            h, w = template.shape[:2]
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2
            if debug:
                highlight_area(top_left[0], top_left[1], w, h)
            print(f"[INFO] Imagem encontrada em ({center_x}, {center_y})")
            return (center_x, center_y, w, h)
        if debug:
            print(f"[DEBUG] Tempo de espera: {elapsed:.2f}s / Tempo limite: {timeout}s")
        if elapsed > timeout:
            print("[AVISO] Imagem não encontrada no tempo limite.")
            return None
        time.sleep(1)

@wait_until_all_ok
def wait(image_path, timeout=10, confidence=0.8, debug=DEBUG, region=None):
    """
    Espera até que uma imagem apareça na tela (ou região) ou até esgotar o tempo.

    - image_path: caminho da imagem a ser encontrada
    - timeout: tempo máximo em segundos
    - confidence: limiar mínimo de similaridade
    - debug: se True, exibe prints e destaque visual
    - region: tupla (x, y, w, h) opcional, define a área de busca

    Retorna:
    - (x, y): centro da imagem encontrada, ou None se não encontrada no tempo limite.
    """

    start_time = time.time()
    total_pause_time = 0

    # Carrega o template uma vez fora do loop
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    while True:
        pause_start = time.time()
        wait_if_paused_or_error()
        pause_end = time.time()
        total_pause_time += pause_end - pause_start

        elapsed = time.time() - start_time - total_pause_time

        # Captura da tela ou região
        if region:
            rx, ry, rw, rh = region
            screenshot = ImageGrab.grab(bbox=(rx, ry, rx + rw, ry + rh))
        else:
            screenshot = pyautogui.screenshot()
            rx, ry = 0, 0  # caso seja tela cheia

        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if debug:
            print(f"[DEBUG] Similaridade: {max_val:.3f}")

        if max_val >= confidence:
            top_left = (max_loc[0] + rx, max_loc[1] + ry)
            h, w = template.shape[:2]
            center_x = top_left[0] + w // 2
            center_y = top_left[1] + h // 2

            if debug:
                highlight_area(top_left[0], top_left[1], w, h)

            print(f"[INFO] Imagem encontrada em ({center_x}, {center_y})")
            return (center_x, center_y, w, h)

        if debug:
            print(f"[DEBUG] Tempo de espera: {elapsed:.2f}s / Tempo limite: {timeout}s")

        if elapsed > timeout:
            print("[AVISO] Imagem não encontrada no tempo limite.")
            return None

        time.sleep(1)

def master_find(image_path, confidence=0.8, debug=DEBUG, region=None):
    """
    Procura uma imagem na tela ou em uma região especificada.
    
    Parâmetros:
    - image_path: caminho da imagem a procurar.
    - confidence: limiar de similaridade (0 a 1).
    - debug: se True, imprime informações e destaca a área.
    - region: tupla opcional (x, y, w, h) para limitar a área de busca.
    
    Retorna:
    - (x, y, w, h): região imagem encontrada, ou None.
    """
    if region:
        x, y, w, h = region
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    else:
        screenshot = pyautogui.screenshot()
        x, y = 0, 0  # origem da tela
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if debug:
        print(f"[DEBUG] Similaridade: {max_val:.3f}")
    if max_val >= confidence:
        top_left = (max_loc[0] + x, max_loc[1] + y)
        h, w = template.shape[:2]
        center_x = top_left[0] + w // 2
        center_y = top_left[1] + h // 2
        if debug:
            highlight_area(top_left[0], top_left[1], w, h)
        return (top_left[0], top_left[1], w, h)
    return None

find=wait_until_all_ok(master_find)

def master_exists(image_path, confidence=0.8, debug=DEBUG, region=None):
    """
    Verifica se uma imagem está presente na tela.
    Retorna True se encontrada, False caso contrário.
    """
    return master_find(image_path, confidence=confidence, debug=debug, region=region) is not None

exists = wait_until_all_ok(master_exists)

@wait_until_all_ok
def list_all(image_path, confidence=0.8, debug=DEBUG, min_distance=10):
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

@wait_until_all_ok
def find_all(image_path, confidence=0.8, debug=DEBUG, min_distance=10):
    """
    Encontra todas as ocorrências da imagem na tela.
    Retorna uma lista com as regiões (x, y, w, h) encontradas.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    h, w = template.shape[:2]

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    y_coords, x_coords = np.where(result >= confidence)

    regions = []
    for (x, y) in zip(x_coords, y_coords):
        # Verifica se já existe uma região próxima
        is_duplicate = any(
            abs(x - rx) < min_distance and abs(y - ry) < min_distance
            for (rx, ry, rw, rh) in regions
        )
        if not is_duplicate:
            regions.append((x, y, w, h))
            if debug:
                highlight_area(x, y, w, h)

    if debug:
        print(f"[INFO] {len(regions)} ocorrência(s) encontradas.")

    return regions

def master_wait_until_disappear(image_path, timeout=15, confidence=0.9, region=None):
    """
    Espera até uma imagem desaparecer da tela.

    - image_path: caminho da imagem
    - timeout: tempo máximo em segundos
    - confidence: precisão do match (0 a 1)

    Retorna True se desapareceu, False se ainda estava na tela após o timeout.
    """
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time 
        if not master_exists(image_path, confidence=confidence, region=region):
            print(f"[VISÃO] Imagem '{image_path}' desapareceu.")
            return True
        if elapsed> timeout:
            print(f"[VISÃO] Timeout. Imagem '{image_path}' ainda está visível.")
            return False
        time.sleep(1)

@wait_until_all_ok
def wait_until_disappear(image_path, timeout=15, confidence=0.9, region=None):
    """
    Espera até uma imagem desaparecer da tela.

    - image_path: caminho da imagem
    - timeout: tempo máximo em segundos
    - confidence: precisão do match (0 a 1)

    Retorna True se desapareceu, False se ainda estava na tela após o timeout.
    """
    start_time = time.time()
    total_pause_time = 0
    while True:
        pause_start = time.time()
        wait_if_paused_or_error()
        pause_end = time.time()
        total_pause_time += pause_end - pause_start
        elapsed = time.time() - start_time - total_pause_time
        if not exists(image_path, confidence=confidence, region=region):
            print(f"[VISÃO] Imagem '{image_path}' desapareceu.")
            return True
        if elapsed> timeout:
            print(f"[VISÃO] Timeout. Imagem '{image_path}' ainda está visível.")
            return False
        time.sleep(1)

@wait_until_all_ok
def check_right(position, image_path, offset=(20, -20), region_size=(100, 40), confidence=0.8, debug=DEBUG):
    """
    Para cada posição, verifica se a imagem está à direita e clica se encontrar.

    - positions: (x, y)
    - image_path: imagem a ser procurada
    - offset: deslocamento da região relativa à posição base
    - region_size: tamanho da área onde buscar a imagem (w, h)
    - confidence: limiar de similaridade
    - debug: se True, imprime e destaca

    Retorna: lista de posições onde o clique foi feito.
    """

    x, y = position
    dx, dy = offset
    rw, rh = region_size
    rx = x + dx
    ry = y + dy

    region = (rx, ry, rw, rh)
    highlight_area(rx, ry, rw, rh)
    result = find(image_path, confidence=confidence, debug=debug, region=region)
    
    if result:
        center_x = result[0] + result[2] // 2
        center_y = result[1] + result[3] // 2
        return (center_x, center_y)
    else:
        if debug:
            print(f"[DEBUG] Imagem '{image_path}' não encontrada na região {region}.")
        return None

class RegionChangeObserver:
    def __init__(self, region, threshold=1000, interval=0.5, debug=DEBUG):
        """
        :param region: (x, y, w, h) da área a ser observada
        :param threshold: número mínimo de pixels diferentes para considerar mudança
        :param interval: tempo entre capturas em segundos
        :param debug: imprime informações
        """
        self.region = region
        self.threshold = threshold
        self.interval = interval
        self.debug = debug
        self._stop_event = threading.Event()
        self._changed = False
        self._thread = None

    def _observe_loop(self):
        x, y, w, h = self.region
        screenshot1 = pyautogui.screenshot(region=(x, y, w, h))
        screenshot1 = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_RGB2BGR)

        while not self._stop_event.is_set():
            time.sleep(self.interval)
            screenshot2 = pyautogui.screenshot(region=(x, y, w, h))
            screenshot2 = cv2.cvtColor(np.array(screenshot2), cv2.COLOR_RGB2BGR)

            diff = cv2.absdiff(screenshot1, screenshot2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
            changed_pixels = cv2.countNonZero(thresh)

            if self.debug:
                print(f"[Observer] Mudança detectada: {changed_pixels} pixels")

            if changed_pixels > self.threshold:
                self._changed = True
                break

    def start(self):
        self._stop_event.clear()
        self._changed = False
        self._thread = threading.Thread(target=self._observe_loop)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()

    def get_result(self):
        return self._changed