import pygame
import sys
from pathlib import Path
import json
# Ustawienia siatki i okna

CELL_SIZE = 40
GRID_ROWS = 30
GRID_COLS = 20
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE

# Stałe przykładowych nagród (możesz je później wykorzystać w symulacji)
START_ROW, START_COL = 29, 19
DEATH_REWARD = -1000
STAGNATION_REWARD = -1
GOAL_REWARD = 1000
APPLE1_REWARD = 10
APPLE2_REWARD = 15
NOTHING_REWARD = -1
VISIBILITY = 3 # ograniczenie widoczności agenta
DRAW = True

# Funkcja ładująca pojedynczy obrazek i skalująca go do rozmiaru komórki
def load_image(file_name, scale=(CELL_SIZE, CELL_SIZE)):
    image = pygame.image.load(file_name).convert_alpha()
    return pygame.transform.scale(image, scale)

# Funkcja ładująca wszystkie obrazki z folderu assets
def load_images():
    assets_folder = Path("assets")
    images = {
        "AGENT": load_image(assets_folder / "agent.png"),
        "WALL": load_image(assets_folder / "wall.png"),
        "GOAL": load_image(assets_folder / "goal.png"),
        "CANNON1": load_image(assets_folder / "cannon_type1.png"),
        "CANNON2": load_image(assets_folder / "cannon_type2.png"),
        "CANNONBALL1": load_image(assets_folder / "cannonball1.png"),
        "CANNONBALL2": load_image(assets_folder / "bouncycannonball.png"),
        "APPLE1": load_image(assets_folder / "apple.png"),
        "APPLE2": load_image(assets_folder / "goldenapple.png")
    }
    return images


