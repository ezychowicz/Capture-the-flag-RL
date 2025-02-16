import pygame
from map import Map
from agent import Agent
# from config import WINDOW_HEIGHT, WINDOW_WIDTH, GRID_ROWS, GRID_COLS, DRAW, VISIBILITY
import config
from randompolicy import RandomPolicy
from simulation import Simulation
from epoch import Epoch
from qlearning import Qlearning
from dqnstrategy import DQNStrategy
from generators import peaceful_generator
import json

def load_map():
    world_list = []
    with open("trainingdata/grid.json", "r") as data:
        world_list = json.load(data)
    game_map = Map(config.GRID_ROWS, config.GRID_COLS)
    for row_cnt, row in enumerate(world_list):
        for col_cnt, col in enumerate(row):
            if col == "CANNON1":
                game_map.addCannon(1, 3, col_cnt)
            elif col == "CANNON2":
                game_map.addCannon(2, 2, col_cnt)
            elif col == "APPLE1":
                game_map.addApple(row_cnt, col_cnt, 1)  
            elif col == "APPLE2":
                game_map.addApple(row_cnt, col_cnt, 2) 
            elif col == "WALL":
                game_map.addWall(row_cnt, col_cnt)
            elif col == "GOAL":
                game_map.addGoals([(row_cnt, col_cnt)])  # Zbieramy cele do dodania na końcu


    return game_map

# def create_map():
#     game_map = Map(GRID_ROWS, GRID_COLS) 
#     game_map.addCannon(1, 1, 0)
#     game_map.addCannon(2, 1, 1)
#     game_map.addCannon(1, 5, 4)
#     game_map.addCannon(1, 2, 6)
#     game_map.addCannon(1, 3, 9)
#     game_map.addCannon(3, 10, 11)
#     game_map.addCannon(4, 1, 15)
#     game_map.addCannon(5, 1, 19)
#     game_map.addApple(10, 10,1)
#     game_map.addApple(5,10,2)
#     game_map.addApple(1,19,2)
#     game_map.addApple(1,0,2)
#     game_map.addWall(10,15)
#     game_map.addWall(10,16)
#     game_map.addWall(10,17)
#     game_map.addWall(10,18)
#     game_map.addWall(10,19)
#     game_map.addWall(13,2)
#     game_map.addWall(13,3)
#     game_map.addWall(13,4)
#     game_map.addWall(2,1)
#     game_map.addWall(2,3)
#     game_map.addWall(2,7)
#     game_map.addWall(6,8)
#     game_map.addWall(2,3)
#     game_map.addWall(2,14)
#     game_map.addGoals([(1,2), (1, 10)])
#     return game_map

def main():
    screen, clock = None, None
    if config.DRAW:
        pygame.init()
        screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("simulation")
        clock = pygame.time.Clock()

    generator = peaceful_generator.PeacefulGenerator()
    game_map = generator.generateMap()
    config.GRID_ROWS = generator.gridRows
    config.GRID_COLS = generator.gridCols 
    config.START_ROW = config.GRID_ROWS - 1
    config.START_COL = config.GRID_ROWS - 1
    simulation = Simulation(DQNStrategy(4*config.VISIBILITY**2 + 2, 9), game_map) 
    epoch = Epoch(screen, game_map, simulation, clock, draw = True)
    maxG = -200
    for episode in range (10000):
        G = epoch.runEpisode()
        print(G)
        maxG = max(maxG, G)
        generator = peaceful_generator.PeacefulGenerator()
        game_map = generator.generateMap()
        simulation.cnt = 0
    print(maxG)
    pygame.quit()

if __name__ == '__main__':
    main()