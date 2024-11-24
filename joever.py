import pygame
import sys

# Initialize pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Audio Buttons")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Button setup
button_width = 150
button_height = 50
button_y_offset = 10
buttons = []

# Load audio files
audio_files = [
    './music/morning.mp3',
    './music/afternoon.mp3',
    './music/nighttime.mp3',
    './music/bedtime.mp3',
]

button_image = pygame.image.load("./graphics/coquette.png")
button_image = pygame.transform.scale(button_image, (100, 100))

# Button class to create clickable buttons
class Button:
    def __init__(self, x, y, width, height, audio_file):
        self.rect = pygame.Rect(x, y, width, height)
        self.audio_file = audio_file

    def draw(self):
        # Draw the image on the button area
        screen.blit(button_image, self.rect.topleft)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            pygame.mixer.stop()
            pygame.mixer.Sound(self.audio_file).play()
            print("clicked")

# Create buttons
for i in range(4):
    button_x = (screen_width - button_width) // 2
    button_y = button_y_offset + (i * (button_height + 42))
    button = Button(button_x, button_y, button_width, button_height, audio_files[i])
    buttons.append(button)

# render text
def render_text(text, offset):
    font = pygame.font.Font(None, 42)
    text_surface = font.render(text, True, 'green')
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - (offset*1.2 + 50)))
    screen.blit(text_surface, text_rect)

# Game loop
running = True
line_1 = "In the day time.. Im Zakary. Just a normal boy with a normal life!"
line_2 = "but There's something about me that no one knows yet 'cause I have a secret"
line_3 = "I AM DEPRESSED ! MEDICINE-LESS MY CAT DIED ON DAY FOUR OF MARCH"
line_4 = "I AM DEPRESSED!!! ENERGY-LESS MY CELLO ROTS IN A CORNER I AM DEPRESED"
while running:
    screen.fill('red')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.check_click(event.pos)

    # Draw buttons
    for button in buttons:
        button.draw()

    render_text(line_1, 160)
    render_text(line_2, 120)
    render_text(line_3, 80)
    render_text(line_4, 40)

    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
