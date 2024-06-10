import pygame
import globals # константи, які потрібні в різних модулях
import time # потрібно для відслідковуваня реального FPS

pygame.init()
sc = pygame.display.set_mode((globals.WW, globals.WH)) # головне полотно

header = pygame.image.load("images/header.png").convert_alpha() # мені нема куди їх впихнутиd
bgClear = pygame.image.load("images/bgClear.png").convert_alpha()
bgClear = pygame.transform.scale(bgClear, (globals.WW, globals.WH))
myFont = pygame.font.Font("fonts/Minecraftia-Regular.ttf", 26) # підключення піксельного шрифта

import platforms # завантажую саме середовище, тому що при кожній новій грі я створюю новий клас
from buttons import buttons
from backgrounds import backgrounds
import clouds
import circle

clock = pygame.time.Clock()

def mainMenuVisual():
    backgrounds.draw(sc, 1) # фон головного меню
    buttons.draw(sc, 0) # startButton
    buttons.draw(sc, 1)  # settingsButton

def mainMenuCheck(event):
    if (event.type == pygame.MOUSEBUTTONDOWN):  # обробка кнопок
        mousePos = pygame.mouse.get_pos()
        buttons.isPressed(mousePos, 0)  # буде перевірятись кнопка з масиву buttons з індексом 0
        buttons.isPressed(mousePos, 1)
    if (event.type == pygame.MOUSEBUTTONUP):
        mousePos = pygame.mouse.get_pos()
        buttons.isUnpressed(mousePos, 0)
        buttons.isUnpressed(mousePos, 1)
def mainMenuLogic():
    pass

def gameStartedVisual():
    sc.fill(globals.LIGHTBLUE)
    clouds.clouds.draw(sc)
    platforms.platforms.draw(sc)
    circle.circle.draw(sc)
    sc.blit(header, (0, 0))
    sc.blit(circle.circle.scoreText, (20, 10))
    if circle.circle.pause:
        sc.blit(bgClear, (0, 0))
        buttons.draw(sc, 4)
        buttons.draw(sc, 5)

def gameStartedCheck(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            circle.circle.k_left = True # прапорець, щоб можна було хажати клавішу вліво
        elif event.key == pygame.K_RIGHT:
            circle.circle.k_right = True# прапорець, щоб можна було хажати клавішу вправо
        elif event.key == pygame.K_ESCAPE:
            circle.circle.pause = not circle.circle.pause # перевірка на паузу
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            circle.circle.k_left = False
        elif event.key == pygame.K_RIGHT:
            circle.circle.k_right = False
        circle.circle.stopped = False
    if circle.circle.pause:
        if (event.type == pygame.MOUSEBUTTONDOWN):  # обробка кнопок
            mousePos = pygame.mouse.get_pos()
            buttons.isPressed(mousePos, 4)
            buttons.isPressed(mousePos, 5)
        if (event.type == pygame.MOUSEBUTTONUP):
            mousePos = pygame.mouse.get_pos()
            buttons.isUnpressed(mousePos, 4)
            buttons.isUnpressed(mousePos, 5)

def gameStartedLogic():
    if not circle.circle.pause:
        clouds.clouds.move()

        if circle.circle.k_left:
            circle.circle.moveLeft()
        elif circle.circle.k_right:
            circle.circle.moveRight()
        elif not circle.circle.stopped:
            circle.circle.stop()
        circle.circle.moveDown()
        circle.circle.collision()
        platforms.platforms.logic()
    else:
        pass

def gameOverVisual():
    backgrounds.draw(sc, 2) # фон при програші
    sc.blit(circle.circle.scoreText, (157, 368))
    buttons.draw(sc, 2) # restart button
    buttons.draw(sc, 3)  # mainMenu button
def gameOverCheck(event):
    if (event.type == pygame.MOUSEBUTTONDOWN):  # обробка кнопок
        mousePos = pygame.mouse.get_pos()
        buttons.isPressed(mousePos, 2)  # буде перевірятись restartButton
        buttons.isPressed(mousePos, 3)  # буде перевірятись mainMenuButton
    if (event.type == pygame.MOUSEBUTTONUP):
        mousePos = pygame.mouse.get_pos()
        buttons.isUnpressed(mousePos, 2)
        buttons.isUnpressed(mousePos, 3)

def gameOverLogic():
    pass



gameModes = ((mainMenuVisual,mainMenuCheck, mainMenuLogic), (gameStartedVisual, gameStartedCheck, gameStartedLogic),
             (gameOverVisual,gameOverCheck, gameOverLogic))
def gameVisual():
    gameModes[globals.GAMEMODE][0]()
    pygame.display.flip()

def gameLogic():
    frames = globals.MAXFPS # прапорець, щоб синохронізувати FPS і MAXPS
    realFrames = 0 # підраховує реальну кількість FPS
    startTime = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            gameModes[globals.GAMEMODE][1](event) # перевірки в залежності від режиму гри

        gameModes[globals.GAMEMODE][2]() # дії в залежності від режиму гри




        frames -= globals.FPS
        if frames <= 0: # на 120 MAXFPS і 30 FPS - gameVisual буде виконуватись 0.25 разів
            gameVisual()

            frames = globals.MAXFPS # прапорець скидається

            realTime = time.time() # розрахунок реальної к-сті FPS
            realFrames += 1
            if realTime - startTime >= 1: # раз на секнуду показує справжнє FPS
                print("FPS:",  realFrames / (realTime - startTime))
                realFrames = 0
                startTime = realTime

        clock.tick(globals.MAXFPS) # логіка буде виконуватись з максимальною к-стю FPS (якщо комп стягує)

gameLogic()