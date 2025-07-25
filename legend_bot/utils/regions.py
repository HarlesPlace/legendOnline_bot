import pyautogui

# Dimensões da tela (pegas uma única vez ao carregar o módulo)
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Metades
HALF_WIDTH = SCREEN_WIDTH // 2
HALF_HEIGHT = SCREEN_HEIGHT // 2

# Regiões nomeadas da tela
BOTTOM_BAR = (0, HALF_HEIGHT, SCREEN_WIDTH, HALF_HEIGHT)
TOP_BAR = (0, 0, SCREEN_WIDTH, HALF_HEIGHT)
CENTER = (int(SCREEN_WIDTH * 0.25), int(SCREEN_HEIGHT * 0.25),
          int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5))
LEFT_SIDE = (0, 0, int(SCREEN_WIDTH * 0.5), SCREEN_HEIGHT)
RIGHT_SIDE = (int(SCREEN_WIDTH * 0.5), 0, int(SCREEN_WIDTH * 0.5), SCREEN_HEIGHT)
FULL_SCREEN = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Quadrantes da tela
TOP_LEFT = (0, 0, HALF_WIDTH, HALF_HEIGHT)
TOP_RIGHT = (HALF_WIDTH, 0, HALF_WIDTH, HALF_HEIGHT)
BOTTOM_LEFT = (0, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT)
BOTTOM_RIGHT = (HALF_WIDTH, HALF_HEIGHT, HALF_WIDTH, HALF_HEIGHT)