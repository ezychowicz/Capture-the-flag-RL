import pygame
from map import Map
from world_elements.agent import Agent
# from config import WINDOW_HEIGHT, WINDOW_WIDTH, GRID_ROWS, GRID_COLS, DRAW, VISIBILITY
import config
from randompolicy import RandomPolicy
from simulation import Simulation
from epoch import Epoch
from qlearning import Qlearning
from dqnstrategy import DQNStrategy
from generators import peaceful_generator, singular_cannon_generator, multiple_cannons_generator, cannons_apples_generator
import json


def load_map():
    world_list = []
    with open("pregenerated_data/grid.json", "r") as data:
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

def game_map_generator(generatorClass, num_maps):
    for _ in range(num_maps):
        generator = generatorClass()
        game_map = generator.generateMap()
        config.GRID_ROWS = generator.gridRows
        config.GRID_COLS = generator.gridCols 
        config.START_ROW = config.GRID_ROWS - 1
        config.START_COL = config.GRID_COLS - 1
        yield game_map

def main():
    screen, clock = None, None
    if config.DRAW:
        pygame.init()
        screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("simulation")
        clock = pygame.time.Clock()

    # training
    maxG = -200
    for typeOfMap in [singular_cannon_generator.SingularCannon, multiple_cannons_generator.MultipleCannons, cannons_apples_generator.CannonsApples]: #peaceful_generator.PeacefulGenerator,
        for game_map in game_map_generator(typeOfMap, 5):
            simulation = Simulation(Qlearning(), game_map)  # DQNStrategy(4*config.VISIBILITY**2 + 2, 9)
            epoch = Epoch(screen, game_map, simulation, clock, draw = True)
            for episode in range (100):
                G = epoch.runEpisode()
                print(G)
                maxG = max(maxG, G)
                simulation.cnt = 0
    print(maxG)

    # benchmark
    generator = peaceful_generator.PeacefulGenerator()
    game_map = generator.generateMap()
    config.GRID_ROWS = generator.gridRows
    config.GRID_COLS = generator.gridCols 
    config.START_ROW = config.GRID_ROWS - 1
    config.START_COL = config.GRID_COLS - 1
    game_map = load_map()
    simulation = Simulation(Qlearning(), game_map)  # DQNStrategy(4*config.VISIBILITY**2 + 2, 9)
    epoch = Epoch(screen, game_map, simulation, clock, draw = True)
    for episode in range (100):
        G = epoch.runEpisode()
        print(G)
        maxG = max(maxG, G)
        simulation.cnt = 0
    pygame.quit()

if __name__ == '__main__':
    main()