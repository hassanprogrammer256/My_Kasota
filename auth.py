import pygame
import pygwidgets
import sys
import os
from constants import *
from dotenv import load_dotenv

load_dotenv()

class Auth:
    def __init__(self, window):
        self.window = window
        self.is_authenticated = False
        self.clock = pygame.time.Clock()

        try:
            self.background_img = pygame.image.load('images/welcome.png')
            self.background_img = pygame.transform.scale(self.background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.mixer.music.load('sounds/crickets.wav')
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.1)
            game_icon = pygame.image.load('images/LOGO.ico')
            pygame.display.set_icon(game_icon)
            
        except Exception as e:
            print(f"Error occurred while loading Game: {e}")
            self.background_img = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background_img.fill(BLACK)

        self.CORRECT_PIN = os.getenv("PIN")
        
        self.pin_entry = pygwidgets.InputText(
            window, 
            (150, WINDOW_HEIGHT//2 - 200),
            '',
            width=600,
            fontSize=150,
            initialFocus=True,
            focusColor=BLACK
        )
        
        self.submit_pin_btn = pygwidgets.TextButton(
            window,
            (250, 300),
            'SUBMIT',
            400,
            textColor=YELLOW,
            fontSize=50,
            height=60,
            upColor=BLACK,
            enterToActivate=True
        )
        
        self.error_display = pygwidgets.DisplayText(
            window, 
            (150, WINDOW_HEIGHT//2 + 150),
            '',
            fontSize=36,
            textColor=RED,
            width=500
        )
        
        self.title = pygwidgets.DisplayText(
            window,
            (150, WINDOW_HEIGHT//2 - 250),
            'Enter PIN to Play MY KASOTA',
            fontSize=48,
            textColor=WHITE,
            width=600
        )
        
        self.error_message = ''
        
    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            self.pin_entry.handleEvent(event)
            
            if self.submit_pin_btn.handleEvent(event):
                entered_pin = self.pin_entry.getValue()
                if entered_pin == self.CORRECT_PIN:
                    self.is_authenticated = True
                    return True
                else:
                    self.error_message = 'Incorrect PIN'
                    self.pin_entry.setValue('')
                    self.error_display.setValue(self.error_message)
                    
        return None
    
    def draw(self):
        self.window.blit(self.background_img, (0, 0))
        self.title.draw()
        self.error_display.draw()
        self.pin_entry.draw()
        self.submit_pin_btn.draw()
        
    def run(self):
        running = True
        
        while running:
            events = pygame.event.get()

            result = self.handleEvents(events)

            if result is False:
                return False
            elif result is True:
                return True

            self.draw()

            pygame.display.update()
     
            self.clock.tick(FPS)
    
        return self.is_authenticated