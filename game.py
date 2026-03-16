from constants import *
from snake import Snake
from food import Food
import pygame,sys,os
from pygame.locals import *
from auth import Auth

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('My Kasota Game By -> Hassan')
        self.window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.mixer.music.load('sounds/crickets.wav')
        game_icon = pygame.image.load('images/LOGO.ico')
        self.background_img = pygame.image.load('images/welcome.png')
        self.background_img = pygame.transform.scale(self.background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_icon(game_icon)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)
        self.snake = Snake(self.window)
        self.fruit = Food(self.window)
        self.is_GameOver = False
        self.is_GamePaused = False
        self.Score  = 0
        self.font =  pygame.font.SysFont('elephant',size=25)
        self.clock = pygame.time.Clock()
        self.is_authenticated = False
        self.error_message = ''
        self.CORRECT_PIN = os.getenv("PIN") 
        self.auth_page = Auth(self.window)
        
    def reset_Game(self):
        self.snake.reset()
        self.fruit.get_random_position()
        self.Score  = 0
        self.is_GameOver=False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
                
            if self.is_authenticated:
                if event.type == KEYUP:
                    if self.is_GameOver:
                        if event.key == K_ESCAPE:
                            return False
                        elif event.key == K_SPACE:
                            self.reset_Game()
                    if event.key == K_ESCAPE:
                        self.is_GamePaused = not self.is_GamePaused
                        
                    if not self.is_GamePaused:
                        if event.key == K_RIGHT:
                            self.snake.change_direction(RIGHT)
                        if event.key == K_LEFT:
                            self.snake.change_direction(LEFT)
                        if event.key == K_UP:
                            self.snake.change_direction(UP)
                        if event.key == K_DOWN:
                            self.snake.change_direction(DOWN)
            else:
                self.auth_page.handleEvent(event)
                
        return True
        
    def update(self):
        if self.is_GameOver or self.is_GamePaused:
            return
        self.snake.move()
        if self.snake.has_eaten_food(self.fruit.food_rect):
            self.snake.grow()
            self.Score += 5
            self.fruit.get_random_position()
        
        while any(segment.colliderect(self.fruit.food_rect) for segment in self.snake.body):
            self.fruit.get_random_position()
            
        if self.snake.check_collision():
            self.is_GameOver = True
            return
            
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.window, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.window, GRAY, (0, y), (WINDOW_WIDTH, y))
            
    def draw_ui(self):
        score_text = self.font.render(f"SCORE:  {self.Score}", True, TEXT_COLOR)
        controls = self.font.render(f"ESC: PAUSE", True, TEXT_COLOR)
        
        self.window.blit(score_text, (10, 10))
        self.window.blit(controls, (WINDOW_WIDTH - 200, 10))
           
    def draw_gameOver(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(BLACK)
        self.window.blit(overlay, (0, 0))
        
        game_over_text = self.font.render('GAME OVER', True, RED)
        score_text = self.font.render(f'SCORE:  {self.Score}', True, TEXT_COLOR)
        restart_text = self.font.render('press SPACE to restart or ESC to quit', True, TEXT_COLOR)
        
        game_over_text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        restart_text_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        
        self.window.blit(game_over_text, game_over_text_rect)
        self.window.blit(score_text, score_text_rect)
        self.window.blit(restart_text, restart_text_rect)
        
    def draw_gamepaused(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(240)
        overlay.fill(BLACK)
        self.window.blit(overlay, (0, 0))    
        
        game_paused_text = self.font.render('PAUSED', True, RED)
        continue_text = self.font.render('press ESC to continue', True, TEXT_COLOR)
        
        game_paused_text_rect = game_paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        continue_text_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        
        self.window.blit(game_paused_text, game_paused_text_rect)
        self.window.blit(continue_text, continue_text_rect)
    
    def draw(self):
        if self.is_authenticated:
            self.window.fill(BLACK)
            self.draw_grid()
            self.draw_ui()
            self.fruit.draw()
            self.snake.draw()
            if self.is_GameOver:
                self.draw_gameOver()
            if self.is_GamePaused and not self.is_GameOver:
                self.draw_gamepaused()
        else:
            self.auth_page.draw()
        
        pygame.display.update()
    
    def run(self):
        running = True
        
        while running:
            if not self.is_authenticated:
                self.is_authenticated = self.auth_page.run()
                pygame.event.clear()

            if self.is_authenticated:
                running = self.handle_events()
                if running:
                    self.update()
                    self.draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()