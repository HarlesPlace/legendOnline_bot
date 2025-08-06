import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

IMG_SIZE = (64, 64)  # Reduzido para ser leve
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset")

def load_data():
    data = []
    labels = []

    for label_name, label_value in [("non_battle", 0), ("battle", 1)]:
        folder = os.path.join(DATASET_PATH, label_name)
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, IMG_SIZE)
            data.append(img.flatten() / 255.0)  # Normaliza
            labels.append(label_value)

    return np.array(data), np.array(labels)

def main():
    print("Carregando dataset...")
    X, y = load_data()

    print(f"Total de imagens: {len(X)}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Treinando o modelo...")
    model = SVC(kernel="linear", probability=True)
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"Acurácia no teste: {acc:.2f}")

    model_path = os.path.join(os.path.dirname(__file__), "battle_detector.joblib")
    joblib.dump(model, model_path)
    print(f"Modelo salvo em: {model_path}")

if __name__ == "__main__":
    main()
