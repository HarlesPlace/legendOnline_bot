import pytesseract
from PIL import ImageOps, ImageGrab, Image
import pyautogui
import time
import cv2, re
import numpy as np
from utils.highlight import highlight_area
from utils.screenVision import find
from core.control import DEBUG, wait_until_all_ok

# Caminho para o executável do Tesseract (ajuste conforme seu sistema)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

@wait_until_all_ok
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

@wait_until_all_ok
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

@wait_until_all_ok
def find_text(target_text, region=None, lang="por", invert=False, debug=DEBUG, color=(0, 0, 255)):
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

@wait_until_all_ok
def extract_text_right_of_image(
    image_path,
    width=100,
    lang="por",
    invert=False,
    debug=DEBUG,
    confidence=0.8,
    only_numbers=False
):
    """
    Encontra uma imagem e extrai texto à direita dela, usando OCR.

    Parâmetros:
    - image_path: caminho da imagem a ser localizada.
    - width: largura da região à direita da imagem que será usada para OCR.
    - lang: idioma a ser usado no OCR (padrão: "por").
    - invert: se True, inverte as cores da imagem para OCR (útil para fundos escuros).
    - debug: se True, destaca visualmente a área e imprime o texto extraído.
    - confidence: nível mínimo de similaridade para reconhecer a imagem.
    - only_numbers: se True, restringe o OCR para detectar apenas dígitos numéricos.

    Retorna:
    - Texto extraído ou None se nada encontrado.
    """
    pos = find(image_path, confidence=confidence, debug=debug)
    if not pos:
        print(f"[ERRO] Imagem '{image_path}' não encontrada.")
        return None

    x, y, w, h = pos
    region_x = x + w
    region_y = y
    region_w = width
    region_h = h

    img = ImageGrab.grab(bbox=(region_x, region_y, region_x + region_w, region_y + region_h))
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    if invert:
        img_cv = cv2.bitwise_not(img_cv)

    config = ""
    if only_numbers:
        config = "--psm 6 -c tessedit_char_whitelist=0123456789"

    text = pytesseract.image_to_string(img_cv, lang=lang, config=config).strip()

    if debug:
        highlight_area(region_x, region_y, region_w, region_h)
        print(f"[OCR] Texto extraído: {text}")

    return text if text else None

@wait_until_all_ok
def extract_text_left_of_image(
    image_path,
    width=100,
    lang="por",
    invert=False,
    debug=DEBUG,
    confidence=0.8,
    only_numbers=False
):
    """
    Encontra uma imagem e extrai texto à esquerda dela, usando OCR.

    Parâmetros:
    - image_path: caminho da imagem a ser localizada.
    - width: largura da região à esquerda da imagem que será usada para OCR.
    - lang: idioma a ser usado no OCR (padrão: "por").
    - invert: se True, inverte as cores da imagem para OCR (útil para fundos escuros).
    - debug: se True, destaca visualmente a área e imprime o texto extraído.
    - confidence: nível mínimo de similaridade para reconhecer a imagem.
    - only_numbers: se True, restringe o OCR para detectar apenas dígitos numéricos.

    Retorna:
    - Texto extraído ou None se nada encontrado.
    """
    pos = find(image_path, confidence=confidence, debug=debug)
    if not pos:
        print(f"[ERRO] Imagem '{image_path}' não encontrada.")
        return None

    x, y, w, h = pos
    region_x = x - width
    region_y = y
    region_w = width
    region_h = h

    # Protege contra valores negativos
    if region_x < 0:
        region_x = 0

    img = ImageGrab.grab(bbox=(region_x, region_y, region_x + region_w, region_y + region_h))
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    if invert:
        img_cv = cv2.bitwise_not(img_cv)

    config = ""
    if only_numbers:
        config = "--psm 6 -c tessedit_char_whitelist=0123456789"

    text = pytesseract.image_to_string(img_cv, lang=lang, config=config).strip()

    if debug:
        highlight_area(region_x, region_y, region_w, region_h)
        print(f"[OCR] Texto extraído: {text}")

    return text if text else None

@wait_until_all_ok
def extract_text_from_position(
    position,
    offset=(100, 0, 150, 50),  # (dx, dy, largura, altura)
    lang="por",
    invert=False,
    debug=DEBUG,
    only_numbers=False,
):
    """
    Extrai texto a partir de uma posição ou região base, usando deslocamento.

    Parâmetros:
    - position: tupla (x, y) ou (x, y, w, h)
    - offset: (dx, dy, w, h) — deslocamento em relação à posição base.
    - lang: linguagem usada pelo Tesseract.
    - invert: inverte as cores (útil para texto claro em fundo escuro).
    - debug: se True, mostra destaque visual da área OCR.
    - only_numbers: se True, restringe o OCR para detectar apenas dígitos numéricos ou %.

    Retorna:
    - número ou texto extraído (como int, float ou string), ou None se nada detectado.
    """
    if len(position) == 2:
        base_x, base_y = position
    elif len(position) == 4:
        base_x, base_y, w, h = position
        base_x = base_x + w  # posiciona OCR à direita da região
        base_y = base_y  # altura será reutilizada mais adiante
    else:
        raise ValueError("A posição deve ser uma tupla com 2 ou 4 valores.")

    dx, dy, ow, oh = offset
    dx, dy, ow, oh = offset

    rx = base_x + dx
    ry = base_y + dy

    img = ImageGrab.grab(bbox=(rx, ry, rx + ow, ry + oh))
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    if invert:
        img_cv = cv2.bitwise_not(img_cv)

    config = ""
    if only_numbers:
        config = "--psm 6 -c tessedit_char_whitelist=0123456789%"

    text = pytesseract.image_to_string(img_cv, lang=lang, config=config).strip()

    if debug:
        highlight_area(rx, ry, ow, oh)
        print(f"[OCR] Texto extraído: {text}")
    
    # Regex: captura número seguido de % (como "75%", "100%")
    if only_numbers:
        match = re.search(r'(\d+(?:[.,]\d+)?)%', text)
        if match:
            return match.group(1).replace(',', '.')  # retorna como string numérica
        else:
            return None

    return text if text else None