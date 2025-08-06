import threading
import time
import joblib
import pyautogui
import cv2
import numpy as np

class BattleDetectorThread(threading.Thread):
    def __init__(self, model_path=None, region=(480, 270, 320, 180), interval=1.0):
        super().__init__()
        self.daemon = True
        self.region = region
        self.interval = interval
        self.in_battle = False
        self.running = True

        if model_path is None:
            model_path = __file__.replace("battleDetection.py", "battle_detector.joblib")
        self.model = joblib.load(model_path)

    def _capture_and_predict(self):
        screenshot = pyautogui.screenshot(region=self.region)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img, (64, 64))
        img_flat = img.flatten() / 255.0
        prediction = self.model.predict([img_flat])[0]
        return prediction == 1  # True se em batalha

    def run(self):
        while self.running:
            try:
                self.in_battle = self._capture_and_predict()
            except Exception as e:
                print(f"[BattleDetector] Erro: {e}")
            time.sleep(self.interval)

    def stop(self):
        self.running = False
