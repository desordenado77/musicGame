#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
import os
import json

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CHANGE_LOOPS = 20


def load_image(nombre, dir_imagen, alpha=False, scale=1):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if scale != 1:
        imgsize = image.get_size()
        image = pygame.transform.scale(image, (int(imgsize[0]*scale), int(imgsize[1]*scale)))
    return image


class Staff(pygame.sprite.Sprite):

    notes = [] # 'c', 'd', 'e', 'f', 'g', 'a', 'b']
    size = []
    position = (0,0)

    def drawme(self):
        self.image.fill((250,250,250))
        self.image.blit(self.keyofg, (0, 0))
        self.rect = self.image.get_rect()
        i =0
        for i in range(1,6):
            pygame.draw.line(self.image, (0,0,0), (0, i*self.rect.height/7),(self.rect.width, i*self.rect.height/7),2)

#        pygame.draw.rect(self.image, (255,0,0), (0,0,self.rect.width, self.rect.height),2)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.keyofg = load_image("keyofg.png", "./", alpha=False)
        self.keyofg = pygame.transform.scale(self.keyofg, (80, 240))
        self.size = self.keyofg.get_size();

        self.image = pygame.Surface([self.size[0]*3, self.size[1]])
        self.drawme()

        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [0, 0]

    def update(self):
        self.drawme()

        i = 0

        for note in self.notes:
            posx = self.size[0]*2  - self.rect.height/7 + ((i%2)*self.rect.height/7)
            i = i+1
            posy = -1
            if note == 'c':
                posy = 12*self.rect.height/14
            if note == 'd':
                posy = 11*self.rect.height/14
            if note == 'e':
                posy = 10*self.rect.height/14
            if note == 'f':
                posy = 9*self.rect.height/14
            if note == 'g':
                posy = 8*self.rect.height/14
            if note == 'a':
                posy = 7*self.rect.height/14
            if note == 'b':
                posy = 6*self.rect.height/14

            if len(self.notes) == 1:
                posx = posx + self.rect.height/7
            if note == 'c':
                pygame.draw.line(self.image, (0,0,0), (posx-self.rect.height/10, posy), (posx+self.rect.height/10, posy),4)
            pygame.draw.circle(self.image, (0,0,0), (posx, posy), self.rect.height/16, 0)


class Keyboard(pygame.sprite.Sprite):

    notes = [] # 'c', 'd', 'e', 'f', 'g', 'a', 'b']
    position = (0,0)

    def drawme(self):
        self.image.fill((250,250,250))
        # white keys
        i =0
        for i in range(0,7):
            pygame.draw.rect(self.image, (0,0,0), (i*(self.rect.width/7),0,(self.rect.width/7), self.rect.height),2)

        # black keys
        pygame.draw.rect(self.image, (0,0,0), ((1*self.rect.width)/14,0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), ((3*self.rect.width)/14,0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), ((7*self.rect.width)/14,0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), ((9*self.rect.width)/14,0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), ((11*self.rect.width)/14,0,(self.rect.width/8), 3*self.rect.height/5),0)


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([300, 180])
        self.rect = self.image.get_rect()

        self.drawme()
        
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [0, 0]

    def update(self):
        self.drawme()
        for note in self.notes:
            posy = 160
            posx = -1
            if note == 'c':
                posx = 1*self.rect.width/14
            if note == 'd':
                posx = 3*self.rect.width/14
            if note == 'e':
                posx = 5*self.rect.width/14
            if note == 'f':
                posx = 7*self.rect.width/14
            if note == 'g':
                posx = 9*self.rect.width/14
            if note == 'a':
                posx = 11*self.rect.width/14
            if note == 'b':
                posx = 13*self.rect.width/14

            if posx != -1:
                pygame.draw.circle(self.image, (255,0,0), (posx, posy), self.rect.width/18, 0)

class NoteName(pygame.sprite.Sprite):

    notes = [] # 'c', 'd', 'e', 'f', 'g', 'a', 'b']
    position = (0,0)

    def drawme(self):
        self.image = pygame.Surface([300, 180], flags=pygame.SRCALPHA)
        self.image.fill((250,250,250, 0))
        self.rect = self.image.get_rect()

    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 50)
        self.font.set_bold(True)
        pygame.sprite.Sprite.__init__(self)
        self.drawme()

        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.speed = [0, 0]

    def update(self):
        self.drawme()

#        pygame.draw.rect(self.image, (0,0,0), (0,0, self.rect.width, self.rect.height), 4)
        displayText = ""
        for note in self.notes:
            posy = 160
            if note == 'c':
                displayText = displayText + "DO "
            if note == 'd':
                displayText = displayText + "RE "
            if note == 'e':
                displayText = displayText + "MI "
            if note == 'f':
                displayText = displayText + "FA "
            if note == 'g':
                displayText = displayText + "SOL "
            if note == 'a':
                displayText = displayText + "LA "
            if note == 'b':
                displayText = displayText + "SI "

        fontRender = self.font.render(displayText, True, (255,0,0))
        self.image.blit(fontRender, ((self.rect.width/2)-fontRender.get_rect().width/2, (self.rect.height/2)-fontRender.get_rect().height/2))


class Mascot(pygame.sprite.Sprite):
    idleImage = []
    runImage = []
    dizzyImage = []
    position = (0,0)
    targetPosition = (0,0)
    dizzyTime = 0
    def drawme(self):
        self.image.fill((255,255,255,0))
        if self.state == 0:
            self.image.blit(self.idleImage[int(self.step)], (0,0))
        elif self.state == 1:
            self.image.blit(self.runImage[int(self.step)], (0,0))
        elif self.state == 2:
            self.image.blit(self.dizzyImage[int(self.step)], (0,0))            

    def run(self):
        self.state = 1
#        self.step = 0

    def idle(self):
        self.state = 0
#        self.step = 0

    def dizzy(self):
        self.state = 2
#        self.step = 0

    def moveTo(self, x, y):
        if ((self.position[0] != self.targetPosition[0]) or (self.position[1] != self.targetPosition[1])) and (self.state == 0):
            self.run()
        self.targetPosition = (x, y)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.idleImage.append(load_image("frame-1.png", "./idle", alpha=True, scale=0.25))
        self.idleImage.append(load_image("frame-2.png", "./idle", alpha=True, scale=0.25))
        self.idleImage.append(load_image("frame-1.png", "./idle", alpha=True, scale=0.25))
        self.idleImage.append(load_image("frame-2.png", "./idle", alpha=True, scale=0.25))
        self.runImage.append(load_image("frame-1.png", "./run", alpha=True, scale=0.25))
        self.runImage.append(load_image("frame-2.png", "./run", alpha=True, scale=0.25))
        self.runImage.append(load_image("frame-3.png", "./run", alpha=True, scale=0.25))
        self.runImage.append(load_image("frame-4.png", "./run", alpha=True, scale=0.25))
        self.dizzyImage.append(load_image("frame-1.png", "./dizzy", alpha=True, scale=0.25))
        self.dizzyImage.append(load_image("frame-2.png", "./dizzy", alpha=True, scale=0.25))
        self.dizzyImage.append(load_image("frame-1.png", "./dizzy", alpha=True, scale=0.25))
        self.dizzyImage.append(load_image("frame-2.png", "./dizzy", alpha=True, scale=0.25))
        self.state = 0 # idle
        # self.state = 1 # run
        self.step = 0
        self.image = pygame.Surface(self.idleImage[0].get_size(), flags=pygame.SRCALPHA)
        self.drawme()


    def update(self):
        newStep = self.step + 0.09
        if newStep >= 4:
            newStep = 0

        if int(newStep) != int(self.step):
            self.step = newStep
            self.drawme()
        else:
            self.step = newStep

        if self.state == 2:
            if self.dizzyTime < 40:
                self.dizzyTime = self.dizzyTime + 1
            else:
                self.dizzyTime = 0
                self.state = 0

        else:
            if self.position[0] < self.targetPosition[0]:
                self.position = (self.position[0] + 1, self.position[1])

            if self.position[1] < self.targetPosition[1]:
                self.position = (self.position[0], self.position[1] + 1)

            if self.position[1] > self.targetPosition[1]:
                self.position = (self.position[0], self.position[1] - 1)

            if (self.position[0] == self.targetPosition[0]) and (self.position[1] == self.targetPosition[1]) and (self.state != 0):
                self.idle()


def main():
    keyArray = {}
    keyArray["c"] = pygame.K_a
    keyArray["d"] = pygame.K_s
    keyArray["e"] = pygame.K_d
    keyArray["f"] = pygame.K_f
    keyArray["g"] = pygame.K_g
    keyArray["a"] = pygame.K_h
    keyArray["b"] = pygame.K_j


    pygame.init()


    with open('pista1.json') as data_file:    
        data = json.load(data_file)

    file = data["Song"]

    print "Song: " + file

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    #pygame.mixer.music.play()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Music Game")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    background_image = load_image("background.png", "./", alpha=False)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background.blit(background_image, (0,0))


    background_green = pygame.Surface(screen.get_size())
    background_green = background_green.convert()
    background_green.fill((255, 250, 255))
    pygame.draw.rect(background_green, (0,255,0), (0,0, SCREEN_WIDTH, SCREEN_HEIGHT), 20)

    background_red = pygame.Surface(screen.get_size())
    background_red = background_red.convert()
    background_red.fill((255, 250, 255))
    pygame.draw.rect(background_red, (255,0,0), (0,0, SCREEN_WIDTH, SCREEN_HEIGHT), 20)


    staff = Staff()
    keyboard = Keyboard()
    notename = NoteName()
    mascot = Mascot()

    staff.position = (20 + notename.rect.width/2 - staff.rect.width/2,20)
    keyboard.position = (20 + 20 + notename.rect.width, 20 + staff.rect.height/2 - keyboard.rect.height/2)
    notename.position = (20,staff.rect.height + 40)
    mascot.position = (20, 580)

    screen.blit(background, (0,0))
    screen.blit(background_green, (0,0))
    screen.blit(staff.image, staff.position)
    screen.blit(keyboard.image, keyboard.position)
    screen.blit(notename.image, notename.position)
    screen.blit(mascot.image, mascot.position)

    pygame.display.flip()

    current_notes = []
    i = 0
    changed = 0
    failure = 0

#    mascot.moveTo(900, 580)

    while True:
        if changed != 0:
            current_notes = []
            changed = changed -1
        else:
            if i < len(data["steps"]) and i>=0:
                current_notes = data["steps"][i]["notes"]
            else:
                current_notes = []

        staff.notes = current_notes
        keyboard.notes = current_notes
        notename.notes = current_notes

        mascot.moveTo(((1024-200)/len(data["steps"]))*i+20, 580)
        staff.update()
        keyboard.update()
        notename.update()
        mascot.update()
        screen.blit(background, (0,0))
        if failure == 1:
            background_red.set_alpha(255*changed/CHANGE_LOOPS)
            screen.blit(background_red, (0,0))
        else:    
            background_green.set_alpha(255*changed/CHANGE_LOOPS)
            screen.blit(background_green, (0,0))

        screen.blit(staff.image, staff.position)
        screen.blit(keyboard.image, keyboard.position)
        screen.blit(notename.image, notename.position)
        screen.blit(mascot.image, mascot.position)

        pygame.display.flip()

        if changed == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    keyFound = 0

                    for theNote in current_notes:
                        if event.key == keyArray[theNote]:
                            i = i + 1
                            changed = CHANGE_LOOPS
                            failure = 0                        
                            keyFound = 1
                    if keyFound == 0:
                        if event.key == pygame.K_LEFT:
                            if i - 1 >= 0:
                                i = i - 1
                                changed = CHANGE_LOOPS
                                failure = 1                            

                        elif event.key == pygame.K_RIGHT:
                            if i + 1 < len(data["steps"]):
                                i = i + 1
                            changed = CHANGE_LOOPS
                            failure = 0
                            mascot.run()
                        else:
                            changed = CHANGE_LOOPS
                            failure = 1
                            mascot.dizzy()



if __name__ == "__main__":
    main()