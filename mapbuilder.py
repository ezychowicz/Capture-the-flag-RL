import pygame
import sys
import json
from pathlib import Path

# Ustawienia siatki i okna
CELL_SIZE = 40
GRID_ROWS = 30
GRID_COLS = 20
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE

# Stałe przykładowych nagród (do symulacji lub dalszej logiki)
START_ROW, START_COL = 29, 19
DEATH_REWARD = -1000
STAGNATION_REWARD = -1
ONECOL_REWARD = -5
GOAL_REWARD = 1000
APPLE1_REWARD = 10
APPLE2_REWARD = 15
NOTHING_REWARD = -0.5
VISIBILITY = 5  # ograniczenie widoczności agenta
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

# Klasa odpowiedzialna za interfejs budowania grida
class GridBuilder:
    def __init__(self, rows, cols, cell_size, images):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.images = images
        
        # Inicjujemy grid jako macierz, gdzie każda komórka przechowuje nazwę obiektu lub None
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        
        # Aktualnie wybrany obiekt do umieszczania – domyślnie None (czyli tryb usuwania)
        self.selected_object = None

        # Czcionka do wyświetlania informacji
        self.font = pygame.font.SysFont("Arial", 18)

        # Mapowanie klawiszy numerycznych na typ obiektu
        self.key_mapping = {
            pygame.K_1: "AGENT",
            pygame.K_2: "WALL",
            pygame.K_3: "GOAL",
            pygame.K_4: "CANNON1",
            pygame.K_5: "CANNON2",
            pygame.K_6: "CANNONBALL1",
            pygame.K_7: "CANNONBALL2",
            pygame.K_8: "APPLE1",
            pygame.K_9: "APPLE2",
            pygame.K_0: None  # Klawisz 0 przełącza tryb usuwania
        }

    def draw_grid(self, surface):
        """Rysuje linie siatki."""
        for row in range(self.rows):
            pygame.draw.line(surface, (200, 200, 200), (0, row * self.cell_size), (self.cols * self.cell_size, row * self.cell_size))
        for col in range(self.cols):
            pygame.draw.line(surface, (200, 200, 200), (col * self.cell_size, 0), (col * self.cell_size, self.rows * self.cell_size))
    
    def draw_cells(self, surface):
        """Rysuje obiekty umieszczone w komórkach."""
        for row in range(self.rows):
            for col in range(self.cols):
                obj = self.grid[row][col]
                if obj is not None and obj in self.images:
                    pos = (col * self.cell_size, row * self.cell_size)
                    surface.blit(self.images[obj], pos)
    
    def draw_info(self, surface):
        """Wyświetla aktualny wybór oraz instrukcje."""
        info_text = f"Aktualnie wybrany obiekt: {self.selected_object if self.selected_object is not None else 'USUŃ'}"
        text_surface = self.font.render(info_text, True, (255, 255, 255))
        surface.blit(text_surface, (10, 10))
        
        # Instrukcje – dodano informację o zapisie do JSON (klawisz S)
        instructions = ("Wciśnij klawisze 1-9, aby wybrać obiekt, 0 aby usunąć, "
                        "S aby zapisać do JSON. Kliknij, aby umieścić.")
        instr_surface = self.font.render(instructions, True, (255, 255, 255))
        surface.blit(instr_surface, (10, 30))
    
    def draw(self, surface):
        """Rysuje cały interfejs – najpierw obiekty, potem siatkę, potem informacje."""
        surface.fill((0, 0, 0))  # czyścimy ekran
        self.draw_cells(surface)
        self.draw_grid(surface)
        self.draw_info(surface)

    def handle_keydown(self, key):
        """Zmienia aktualnie wybrany obiekt lub zapisuje grid przy odpowiednim klawiszu."""
        if key in self.key_mapping:
            self.selected_object = self.key_mapping[key]
            print(f"Wybrano: {self.selected_object}")
        elif key == pygame.K_s:
    
            self.save_to_json(Path(__file__).parent / "trainingdata" / "grid.json")
            print("Grid zapisany do grid.json")

    def handle_mouse_click(self, pos):
        """Umieszcza lub usuwa obiekt w klikniętej komórce."""
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = self.selected_object
            print(f"Ustawiono {self.selected_object} w komórce ({row}, {col})")
    
    def save_to_json(self, filename):
        """Zapisuje stan grida do pliku JSON."""
        with open(filename, 'w') as f:
            json.dump(self.grid, f, indent=4)
        print(f"Stan grida zapisany w pliku: {filename}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Grid Builder w Pygame")
    
    # Ładujemy obrazki
    images = load_images()

    # Inicjujemy interfejs budowania grida
    grid_builder = GridBuilder(GRID_ROWS, GRID_COLS, CELL_SIZE, images)

    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(60)  # ograniczenie do 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.KEYDOWN:
                grid_builder.handle_keydown(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # lewy przycisk myszy
                    grid_builder.handle_mouse_click(event.pos)

        grid_builder.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
