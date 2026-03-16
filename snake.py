from constants import *
import pygame,os,sys


class Snake:
    def __init__(self,window:pygame.Surface):
        self.window = window
        self.reset()
          
    def reset(self):
        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        self.body = []
        
        for i in range(INITIAL_SNAKE_LENGTH):
            rect = pygame.Rect(start_x - (i*CELL_SIZE),start_y,CELL_SIZE,CELL_SIZE)
            self.body.append(rect)
        self.direction= RIGHT
        self.grow_flag = False
        
    def move(self):
        head = self.body[0].copy()
        
        if self.direction == RIGHT:
            head.x += CELL_SIZE
        elif self.direction == LEFT:
            head.x -= CELL_SIZE
        elif self.direction == UP:
            head.y -= CELL_SIZE
        elif self.direction == DOWN:
            head.y += CELL_SIZE
            
        self.body.insert(0,head)
        
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
            
    def change_direction(self,new_dir:str) -> str:
        DIR_MAPPINGS = {LEFT:RIGHT, UP:DOWN,RIGHT:LEFT,DOWN:UP}
        if new_dir != DIR_MAPPINGS.get(self.direction):
            self.direction= new_dir
    
    def grow(self):
        self.grow_flag = True
    
    def check_collision(self) -> bool:
        head = self.body[0]
        if (head.x < 0 or head.y < 0 or head.x >= GRID_WIDTH * CELL_SIZE or head.y >= GRID_HEIGHT * CELL_SIZE):
            return True
        for segment in self.body[1:]:
            if head.colliderect(segment):
                return True
        return False
    
    def has_eaten_food(self,food_rect):
        return self.body[0].colliderect(food_rect)
    
    def draw(self):
        for i,segment in enumerate(self.body):
            color = SNAKE_COLOR if i > 0 else (0,0,250)
            pygame.draw.rect(self.window,color,segment)
            pygame.draw.rect(self.window,BLACK,segment,1)
            
        
        
        
# if __name__ == "__main__":
#     pygame.init()
#     window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
#     clock = pygame.time.Clock()
    
#     osnake = Snake(window)
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
                
           
        
#         window.fill((0,0,0,))
        
#         osnake.draw()
        
#         pygame.display.update()
#         clock.tick(FPS)
        
#     pygame.quit()
#     sys.exit()
            