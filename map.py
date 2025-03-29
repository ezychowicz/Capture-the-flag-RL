from world_elements.cannon import Cannon
from world_elements.wall import Wall
from world_elements.apple import Apple
from collections import defaultdict
import pygame
# from config import CELL_SIZE, load_images, GRID_ROWS, GRID_COLS
import config
from world_elements.world_element_encoding import ObjectType
from actions import Action
from collections import deque
class Map:
    def __init__(self, rows, cols):
        self.world = defaultdict(lambda: {"WALL": None, "GOAL": None, "CANNON": None, "CANNONBALL": None, "APPLE": None})
        self.cannons = []
        self.cannonballs = [set() for row in range (config.GRID_ROWS)] # it is necessary to store these separately and in correct order
        self.apples = []
        self.goal = None
        self.height = rows
        self.width = cols
        
    def addCannon(self, step: int, rate: int, col: int):
        self.world[(0, col)]["CANNON"] = Cannon(col, rate, step, self)
        self.cannons.append(self.world[(0, col)]["CANNON"]) 

    def addWall(self, row: int, col: int):
        self.world[(row,col)]["WALL"] = Wall(row, col, self)
        
    def addApple(self, row: int, col: int, type: int):
        if (row, col) not in self.world:
            self.world[(row, col)]["APPLE"] = Apple(type, row, col, self)
            self.apples.append(self.world[(row, col)]["APPLE"])

    def reAddApples(self):
        for apple in self.apples:
            self.world[(apple.row, apple.col)]["APPLE"] = apple
        
    def addGoals(self, positions: list[tuple[int, int]]):
        for pos in positions:
            self.world[pos]["GOAL"] = True # mark as a goal position 
            self.goal = pos
    def getAvailableActions(self, state, agent):
        walls = state[:,:,ObjectType.encode("WALL")] # matrix of walls
        centerRow, centerCol = len(walls)//2, len(walls[0])//2
        available = []
        for vec in (Action.STAY.value, Action.UP.value, Action.DOWN.value, Action.LEFT.value, Action.RIGHT.value, Action.UPRIGHT.value, Action.UPLEFT.value, Action.DOWNRIGHT.value, Action.DOWNLEFT.value):
            if 0 < agent.row + vec[0] < config.GRID_ROWS and 0 <= agent.col + vec[1] < config.GRID_COLS and walls[centerRow + vec[0], centerCol + vec[1]] != 1:
                available.append(vec)
        return available
    
    def drawMap(self, screen):
        images = config.load_images()
        for (row, col), cell in self.world.items():
            x = col * config.CELL_SIZE
            y = row * config.CELL_SIZE
            rect = pygame.Rect(x, y, config.CELL_SIZE, config.CELL_SIZE)
            
            if cell["WALL"] is not None:
                screen.blit(images["WALL"], (x, y))
            if cell["GOAL"]:
                screen.blit(images["GOAL"], (x, y))
            if cell["CANNON"] is not None:
                if cell["CANNON"].step == 1:
                    screen.blit(images["CANNON1"], (x, y))
                else:
                    screen.blit(images["CANNON2"], (x, y))
            if cell["CANNONBALL"] is not None:
                if cell["CANNONBALL"].cannon.step == 1:
                    screen.blit(images["CANNONBALL1"], (x, y))
                else:
                    screen.blit(images["CANNONBALL2"], (x, y))
            if cell["APPLE"] is not None:
                if cell["APPLE"].type == 1:
                    screen.blit(images["APPLE1"], (x, y))
                else:
                    screen.blit(images["APPLE2"], (x, y))
    

