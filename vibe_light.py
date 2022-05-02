import pygame
import itertools

screen_size = (1920, 1080)

# pastel pink
LOW_COLOR = (255,209,220)
# deep blue
MED_COLOR = (7, 42, 108)
# red
PARTY_COLOR = (255, 0, 0)

color_map = {
    'LOW': LOW_COLOR,
    'MED': MED_COLOR,
    'PARTY': PARTY_COLOR
}

class VibeLight:
    def __init__(self):
        self.is_on = False

    def start(self):
        pygame.init()
        self.is_on = True
        self.screen = pygame.display.set_mode(screen_size)

    def set_mood(self, mood):
        self.screen.fill(color_map[mood])
        pygame.display.flip()
