import pygame
import globals
images = ("images/bg.jpg", "images/bgMainMenu.jpg", "images/bgGameOver.jpg")

class Background:
    def __init__(self, src):
        self.img = pygame.image.load(src).convert()
        self.img = pygame.transform.scale(self.img, (globals.WW, globals.WH))

class Backgrounds:
    def __init__(self):
        self.backgrounds = []
        for i in images: # i - шлях до картинки
            self.backgrounds.append(Background(i))
    def draw (self, surf, i):
        surf.blit(self.backgrounds[i].img, (0, 0))

backgrounds = Backgrounds()