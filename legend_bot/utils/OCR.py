import pytesseract
from PIL import ImageOps
import pyautogui
import time
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

        if target_text.lower() in texto_atual.lower():
            print(f"[OCR] Texto encontrado: {target_text}")
            return True

        if elapsed> timeout:
            print(f"[OCR] Timeout. Texto '{target_text}' não encontrado.")
            return False

        time.sleep(1)