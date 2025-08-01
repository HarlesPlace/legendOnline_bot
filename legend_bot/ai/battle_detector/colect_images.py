import cv2
import numpy as np
import pyautogui
import keyboard
import os
import time
from utils.regions import *

BASE_PATH = os.path.dirname(__file__)
SAVE_PATH = os.path.join(BASE_PATH, "dataset")
REGION = BOTTOM_BAR
INTERVAL = 1.0  # segundos entre capturas

def capture_image(region):
    img = pyautogui.screenshot(region=region)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return img

def main():
    print("[S] = salvar como batalha")
    print("[N] = salvar como não-batalha")
    print("[Q] = sair")

    count = {"battle": 0, "non_battle": 0}

    while True:
        print("Aguardando tecla (s/n/q)...")
        while True:
            if keyboard.is_pressed("s"):
                label = "battle"
                break
            elif keyboard.is_pressed("n"):
                label = "non_battle"
                break
            elif keyboard.is_pressed("q"):
                return
            time.sleep(0.05)

        img = capture_image(REGION)
        label_dir = os.path.join(SAVE_PATH, label)
        os.makedirs(label_dir, exist_ok=True)
        filename = f"{label}_{count[label]}.jpg"
        path = os.path.join(label_dir, filename)
        cv2.imwrite(path, img)
        count[label] += 1
        print(f"Imagem salva em: {path}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
