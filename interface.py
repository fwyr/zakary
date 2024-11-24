import pygame 
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.depression_bar_rect = pygame.Rect(10, 10, DEPRESSION_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 44, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, colour):
        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # convert stat to pixel
        current_width = bg_rect.width * (current / max_amount)
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw bar
        pygame.draw.rect(self.display_surface, colour, current_rect)

        # draw half for depression
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 4)


    def show_calendar(self, day, hour, minute):
        text_surface = self.font.render(f"Day {day} | {int(hour):02}H {int(minute):02}M", False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = 20
        text_rect = text_surface.get_rect(topright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20), 3)

    def display(self, player):
        self.show_bar(player.depression, player.stats['depression'], self.depression_bar_rect, DEPRESSION_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        # drawing marker for half-depression
        half_depression_rect = self.depression_bar_rect.copy()
        half_depression_rect.width = 4
        half_depression_rect.height = self.depression_bar_rect.height - 2
        half_depression_rect.center = self.depression_bar_rect.center
        pygame.draw.rect(self.display_surface, 'red', half_depression_rect)

        self.show_calendar(player.day, player.hour, player.minute)

