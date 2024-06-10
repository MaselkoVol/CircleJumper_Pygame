import pygame
FPS = 120 # бажане fps
MAXFPS = 120# максимальне фпс не мінят

WW = 500 # реальний розмір довжини гри гри
WH = 750 # реальний розмір висоти гри

WHITE = (255, 255, 255) # назви кольорів в rgb
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (55, 71, 30)
LIGHTBLUE = (173, 216, 230)

username = input("Enter your name: ")

GAMEMODE = 0 # для вибору режиму гри
score = 0
pygame.mixer.init(44100, -16, 1, 512)
pada = pygame.mixer.Sound("music/pada.wav")
spring = pygame.mixer.Sound("music/feder.wav")
jump = pygame.mixer.Sound("music/jump.wav")
lomise = pygame.mixer.Sound("music/lomise.wav")
button = pygame.mixer.Sound("music/button.wav")