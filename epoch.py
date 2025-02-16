import pygame
# from config import START_COL, START_ROW
import config

class Epoch:
    def __init__(self, screen, worldMap, simulation, clock, draw = True):
        self.reward = 0
        self.screen = screen
        self.worldMap = worldMap
        self.simulation = simulation
        self.clock = clock
        self.draw = draw
    def runEpisode(self):
        running = True
        G = 0
        self.simulation.agent.row, self.simulation.agent.col = config.START_ROW, config.START_COL
        while running:
            if self.draw:
                running = not any(event.type == pygame.QUIT for event in pygame.event.get())
                self.screen.fill((255, 255, 255))
                self.worldMap.drawMap(self.screen)
                self.simulation.agent.drawAgent(self.screen)
                pygame.display.flip()
                self.clock.tick(30)  
            G += self.simulation.update() # accumulate return
            if self.simulation.agent.isDead() or self.simulation.agent.flagCaptured(): 
                break
        return G