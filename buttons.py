import pygame
import platforms
import circle
import globals
import clouds


class Button:
    def __init__ (self, x, y, staticImg, activeImg):
        self.x = x  # центр копки
        self.y = y

        self.staticImg = pygame.image.load(staticImg).convert_alpha()  # ненажата кнопка
        self.activeImg = pygame.image.load(activeImg).convert_alpha() # нажата кнопка
        self.width = self.staticImg.get_width()
        self.height = self.staticImg.get_height()
        self.cur = self.staticImg

    def logic(self):
        pass
class StartButton(Button):
    def logic(self):
        globals.score = 0
        platforms.platforms = platforms.Platforms()
        clouds.clouds = clouds.Clouds()
        lowestPlatform = platforms.platforms.lowestPlatform()
        circle.circle = circle.Circle(lowestPlatform[0] + 20, lowestPlatform[1] - 100)
        globals.GAMEMODE = 1

class MainMenuButton(Button):
    def logic(self):
        globals.GAMEMODE = 0

class PauseButton(Button):
    def logic(self):
        circle.circle.pause = False

class OffButton(Button):
    def logic(self):
        exit()

startButton = StartButton(162, 561, "images/startButton.png", "images/activeStartButton.png")
offButton = OffButton(381, 43, "images/offButton.png", "images/activeOffButton.png")
restartButton = StartButton(276, 561, "images/restartButton.png", "images/activeRestartButton.png")
mainMenuButton = MainMenuButton(47, 561, "images/mainMenuButton.png", "images/activeMainMenuButton.png")
pauseButton = PauseButton(210, 311, "images/pauseButton.png", "images/activePauseButton.png")
pauseExitButton = MainMenuButton(162, 561, "images/mainMenuButton.png", "images/activeMainMenuButton.png")


class Buttons:
    buttons = (startButton, offButton, restartButton, mainMenuButton, pauseButton, pauseExitButton)

    def draw(self, surf, i):
            surf.blit(self.buttons[i].cur, (self.buttons[i].x, self.buttons[i].y))

    def isPressed(self, mousePos, i):
        if mousePos[0] > self.buttons[i].x and mousePos[0] < self.buttons[i].x + self.buttons[i].width:
            if mousePos[1] > self.buttons[i].y and mousePos[1] < self.buttons[i].y + self.buttons[i].height:
                self.buttons[i].cur = self.buttons[i].activeImg
                globals.button.play()
    def isUnpressed(self, mousePos, i):
        self.buttons[i].cur = self.buttons[i].staticImg
        if mousePos[0] > self.buttons[i].x and mousePos[0] < self.buttons[i].x + self.buttons[i].width:
            if mousePos[1] > self.buttons[i].y and mousePos[1] < self.buttons[i].y + self.buttons[i].height:
                self.buttons[i].logic()

buttons = Buttons()

