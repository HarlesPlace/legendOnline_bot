import cv2

coords = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        print(f"Coordenada clicada: ({x}, {y})")
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Mapa", img)

# Substitua pelo caminho da imagem do seu mapa
img = cv2.imread(r"C:\Users\Cliente\Desktop\Pessoal\LegendOnline_bot\legend_bot\images\by_map_go_to\map.png")
cv2.imshow("Mapa", img)
cv2.setMouseCallback("Mapa", click_event)

print("[INFO] Clique nos pontos desejados, pressione ESC para sair.")

while True:
    key = cv2.waitKey(1)
    if key == 27:  # Tecla ESC
        break

cv2.destroyAllWindows()

print("\nCoordenadas coletadas:")
for name, point in enumerate(coords, 1):
    print(f'"ponto{str(name)}": {point},')