import pygame
import globals
import platforms
import clouds
myFont = pygame.font.Font("fonts/Minecraftia-Regular.ttf", 26) # підключення піксельного шрифта
class Circle:
    def __init__ (self, x, y):
        globals.score = 0
        self.scoreText = myFont.render("Score: " + self.getScore(), False, globals.BLACK)
        self.img = pygame.image.load("images/circle.png").convert_alpha()
        self.k_left = self.k_right = self.stopped = self.pause = False # прапорці
        self.x = x # хітбокс
        self.y = y
        self.width = 39
        self.height = 39
        self.speedY = 0
        self.speedX = 0

    def draw(self, surf):
        surf.blit(self.img, (self.x, self.y + 5))

    def moveRight(self):
        if self.speedX < 0:
            self.speedX = 0
        self.x += self.speedX
        if (self.speedX <= 5):
            self.speedX += .1 # щоб плавно нарощувати швидкість до 5 максимум
        if self.x >= globals.WW - 20: # 20 - self.width / 2 (половина довжини)
            self.x = -20
    def moveLeft(self):
        if self.speedX > 0:
            self.speedX = 0
        self.x += self.speedX
        if (self.speedX >= -5):
            self.speedX -= .1
        if self.x <= -20: # 20 - self.width / 2 (половина довжини)
            self.x = globals.WW - 20

    def stop (self):
        if abs(self.speedX) < .2: # якщо швидкість дуже маленька, то дудл зупинився
            self.speedX = 0
            self.stopped = True
        elif self.speedX < 0:
            self.speedX += .2
            self.x += self.speedX
        elif self.speedX > 0:
            self.speedX -= .2
            self.x += self.speedX
    def moveDown(self):
        if self.speedY > 0 and self.y <= 350: # якщо висота менша за 350, то рухається світ. Інакше сам дудл
            platforms.platforms.moveDown(self.speedY + 0.1)
            clouds.clouds.moveDown(self.speedY / 2)
            globals.score += self.speedY // 3
            self.scoreText = myFont.render("Score: " + self.getScore(), False, globals.BLACK)
        elif self.y > globals.WH: # перевірка на програш
            globals.pada.play()
            with open('records.txt', 'a') as recoreds:
                recoreds.write(globals.username + "-" + self.getScore() + "\n")
            globals.GAMEMODE = 2 # перехід до сцени з програшем
        else:
            self.y -= self.speedY
        self.speedY -= 0.1

    def getScore (self): # робить з float - цілеч число з типом str
        return str(int(globals.score))

    def collision (self):
        if self.speedY < 0: # щоб коли дудл летів вгору, колізії не було
            for row in platforms.platforms.platforms:
                if (row and self.y + self.height < row.y + 14 and self.y + self.height > row.y): # 14 - висота платформи
                    # якщо дудл знаходиться в ряді
                    for platform in row.row: # проходиться по кожній платформі

                        if isinstance(platform, platforms.SpringPlatform) and self.x < platform.x + platform.springShift + platform.springWidth and self.x + self.width > platform.x + platform.springShift:
                            # якщо платформа з пружиною, і дудл дотикається до пружини
                            self.speedY = 12
                            platform.cur = platform.activeSpringImg
                            globals.spring.play()
                        elif (self.x < platform.x + platform.width and self.x + self.width > platform.x):
                            # якщо дудл дотикається до платформи
                            if isinstance(platform, platforms.FakePlatform): # якщо це платформа, яка ламається
                                if platform.cur != platform.activeImg:
                                    platform.cur = platform.activeImg
                                    globals.lomise.play()
                            else:
                                globals.jump.play()
                                self.speedY = 7 # з цією швидкістю дудл підлітає
