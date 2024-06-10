import random

import pygame
import globals

class Platform:
    def __init__ (self, x, y, img = "images/platform.png"):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img).convert_alpha()
        self.width = 87
        self.height = 20
    def draw(self, surf):
        surf.blit(self.img, (self.x, self.y))
    def logic(self):
        pass

class SpringPlatform(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.springImg = pygame.image.load("images/spring.png").convert_alpha()
        self.activeSpringImg = pygame.image.load("images/activeSpring.png").convert_alpha()
        self.cur = self.springImg
        self.springWidth = 20
        self.springHeight = 25
        self.springShift = random.randint(0, self.width - self.springWidth)
    def draw (self, surf):
        super().draw(surf)
        surf.blit(self.cur, (self.x + self.springShift, self.y - self.springHeight))

class GlidePlatform (Platform):
    def __init__(self, x, y):
        super().__init__(x, y, "images/glidePlatform.png")
        self.speed = 1 if random.randint(0, 1) else -1
    def logic(self):
        self.x += self.speed
        if (self.x + self.width > globals.WW - 10 or self.x  < 10):
            self.speed = -self.speed

class FakePlatform (Platform):
    def __init__(self, x, y):
        super().__init__(x, y, "images/fakePlatform.png")
        self.activeImg = pygame.image.load("images/activeFallingPlatform.png").convert_alpha()
        self.cur = self.img
    def draw (self, surf):
        surf.blit(self.cur, (self.x, self.y))

class Square: # екраз розбитий на поля, перші 5 з них за екраном
    def __init__ (self):
        self.row = []
        self.y = 0
class Platforms:
    def __init__ (self):
        self.density = 7
        self.squareHeight = globals.WH // 25 # вистота одного ряду плаформ
        self.platforms = []
        self.maxWidth = globals.WW - 90
        self.mul = 0
        for i in range(0, 30): # перші 5 виходять за екран
            self.shift = random.randint(10, 50)
            self.platforms.append(Square())
            self.platforms[i].y = i * self.squareHeight - 150
            self.fillRow(self.platforms[i], self.platforms[i].y)

    def fillRow(self, row, y):
        row.y = y
        if (globals.score > 1000 and not random.randint(0, 25)):
            row.row.append(GlidePlatform(random.randint(10, globals.WW - 88), y))
            self.mul = 0
            if self.density == 7:
                self.density = 4
        else:
            self.shift = random.randint(10, 50)
            while (self.shift < self.maxWidth): # поки платформа не вилазить за правий край вікна
                curChance =self.mul * random.random() * self.density
                if curChance >= 1: # mul постійно зростаєі тим самим збільшує шанс на появу платформи
                    self.mul = 0
                    if random.randint(0, 5):
                        row.row.append(Platform(self.shift, y))
                    else:
                        row.row.append(SpringPlatform(self.shift, y))
                elif curChance > 0.47 and curChance < 0.52:
                    row.row.append(FakePlatform(self.shift, y))
                self.shift += 78 + random.randint(10, 50)  # 78 - довжина платформи
                self.mul += 0.02
    def moveDown(self, speed):
        for row in self.platforms:
            row.y += speed # опускаю весь ряд
            for i in row.row:
                i.y = row.y

            if row.y >= 750 + self.squareHeight: # якщо ряд опустився нище кінця вкіна, то переставляю його на гору
                row.row.clear()
                self.fillRow(row, row.y - 900) # заповнюю ряд платформами

    def draw (self, surf): # малює платформи, які знаходяться в межах екрану
        for row in self.platforms:
            if row.y >= -self.squareHeight:
                for i in row.row:
                    i.draw(surf)
    def logic (self):
        for row in self.platforms:
            if row.y >= -self.squareHeight:
                for i in row.row:
                    i.logic()
    def lowestPlatform(self): # функція використовується лише раз коли починається гра
        lowest = None
        for i in self.platforms:
            if (i.row and not isinstance(i.row[0], FakePlatform)):
                lowest = i.row[0]
        return (lowest.x,lowest.y)