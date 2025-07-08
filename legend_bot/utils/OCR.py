import pytesseract
from PIL import ImageOps, ImageGrab, Image
import pyautogui
import time
import cv2
import numpy as np
from utils.highlight import highlight_area

# Caminho para o executável do Tesseract (ajuste conforme seu sistema)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

def read_text_from_screen(region=None, lang="por", invert=False):
    """
    Captura texto da tela usando OCR.
    region: (left, top, width, height) — define uma área da tela
    lang: idioma do OCR (ex: 'por', 'eng')
    invert: se True, inverte as cores da imagem capturada, bom para fundos escuros.
    """
    screenshot = pyautogui.screenshot(region=region)
    # Converte para tons de cinza
    img = ImageOps.grayscale(screenshot)

    # Inverte as cores, se necessário
    if invert:
        img = ImageOps.invert(img)

    img.save("legend_bot/debugOCR/debug_ocr.png")
    text = pytesseract.image_to_string(screenshot, lang=lang)
    return text.strip()

def wait_for_text(target_text, region=None, lang="por", timeout=15, invert=False):
    """
    Espera até que um texto apareça na tela.
    
    - target_text: texto exato ou trecho esperado
    - region: (x, y, w, h) da área da tela
    - timeout: tempo máximo (em segundos)
    - invert: inverte as cores da imagem se necessário
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

        texto_atual = read_text_from_screen(region=region, lang=lang, invert=invert)
        print(f"[OCR] Verificando texto: '{texto_atual}'")
        if target_text.lower() in texto_atual.lower():
            print(f"[OCR] Texto encontrado: {target_text}")
            return True

        if elapsed> timeout:
            print(f"[OCR] Timeout. Texto '{target_text}' não encontrado.")
            return False

        time.sleep(1)

def preprocess_for_ocr(img_cv, invert=False, upscale=2):
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    if invert:
        gray = cv2.bitwise_not(gray)

    # Aumentar a imagem para melhorar OCR em texto pequeno
    if upscale > 1:
        gray = cv2.resize(gray, None, fx=upscale, fy=upscale, interpolation=cv2.INTER_LINEAR)

    # Aplicar binarização adaptativa
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    return thresh

def find_text(target_text, region=None, lang="por", invert=False, debug=False, color=(0, 0, 255)):
    """
    Procura um texto específico na tela e retorna a posição (x, y, w, h) da região.

    - target_text: texto a procurar (ou parte dele)
    - region: (x, y, w, h) ou None para tela toda
    - lang: idioma usado pelo Tesseract
    - invert: se True, inverte as cores (útil em textos claros no fundo escuro)
    - debug: mostra a área destacada se encontrar
    """
    if region:
        rx, ry, rw, rh = region
        img = ImageGrab.grab(bbox=(rx, ry, rx + rw, ry + rh))
    else:
        rx, ry = 0, 0
        img = ImageGrab.grab()

    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Pré-processa a imagem para OCR
    processed = preprocess_for_ocr(img_cv, invert=invert, upscale=1)

    # Usa modo PSM 6 (assume bloco de texto uniforme)
    data = pytesseract.image_to_data(processed, lang=lang, config="--psm 6", output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data["text"]):
        if target_text.lower() in word.lower():
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]

            # Se usou upscale, converte para coordenadas originais
            scale = 2
            x, y, w, h = x // scale, y // scale, w // scale, h // scale

            abs_x = x + rx
            abs_y = y + ry

            if debug:
                highlight_area(abs_x, abs_y, w, h, duration=2.0)

            return (abs_x, abs_y, w, h)

    return None