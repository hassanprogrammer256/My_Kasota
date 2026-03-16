import pygame,sys,random
from constants import *


class Food:
    def __init__(self,window:pygame.Surface):
        self.window = window
        self.reset()
        self.get_random_position()
        
    def reset(self):
        self.food_x = 0
        self.food_y = 0
        self.food_rect = pygame.Rect(self.food_x,self.food_y,CELL_SIZE,CELL_SIZE)
        
    def get_random_position(self):
        self.food_x = random.randint(0,GRID_WIDTH - 1)
        self.food_y = random.randint(0,GRID_HEIGHT - 1)
        
        self.food_rect.x = self.food_x * CELL_SIZE
        self.food_rect.y = self.food_y * CELL_SIZE
        
        
    def draw(self):
        pygame.draw.rect(self.window,FOOD_COLOR,self.food_rect)
        pygame.draw.rect(self.window,BLACK,self.food_rect,1)
        
        
        
        
        
        
# if  __name__ == "__main__":
#     pygame.init()
#     window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
#     clock = pygame.time.Clock()
    
#     ofruit = Food(window)
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
                
#         window.fill(BLACK)
#         ofruit.draw()
#         pygame.display.flip()
#     pygame.quit()
#     sys.exit()