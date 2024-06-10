import pygame.image
import globals
import random

cloudImgs = ["images/cloud1.png", "images/cloud2.png"]
class Cloud:
    def rebuilCloud (self):
        curRand = random.random() # допоміжна змінна, яка пов'язує швидкість та розмір
        self.speed = (1 / (curRand + 0.1)) / 40 + 0.2
        width = 110 + int(curRand * 20) # розміри нової хмари
        self.img = pygame.image.load(cloudImgs[random.randint(0, len(cloudImgs) - 1)]).convert_alpha()
        self.img = pygame.transform.scale(self.img, (width, self.img.get_height() * width / self.img.get_width()) )
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def __init__(self, x):
        self.x = x
        self.rebuilCloud()
        self.y = random.randint(-750 , 750 - self.height)
    def move (self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = random.randint(globals.WW, 750)
            self.y = random.randint(-globals.WH, globals.WH - self.height)
    def moveDown(self, speed):
        self.y += speed
        if self.y > globals.WH:
            self.rebuilCloud()
            self.y -= globals.WH + random.randint(self.height, 750)
            self.x = random.randint(0, 750)

class Clouds:
    def __init__ (self):
        self.clouds = []

        counter = 100 + random.randint(0, 100) # допоміжна змінна, щоб хмари розташовувались по порядку
        for i in range(3):
            self.clouds.append(Cloud(counter))
            counter += 100 + random.randint(0, 100)

    def draw (self, surf):
        for i in self.clouds:
            if (i.x < globals.WW):
                surf.blit(i.img, (i.x, i.y))

    def moveDown(self, speed):
        for i in self.clouds:
            i.moveDown(speed)
    def move (self):
        for i in self.clouds:
            i.move()




