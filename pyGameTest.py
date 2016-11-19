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


def load_image(nombre, dir_imagen, alpha=False):
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
    return image


class Staff(pygame.sprite.Sprite):

    notes = [] # 'c', 'd', 'e', 'f', 'g', 'a', 'b']
    size = []

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

    def drawme(self):
        self.image.fill((250,250,250))
        # white keys
        i =0
        for i in range(0,7):
            pygame.draw.rect(self.image, (0,0,0), (i*(self.rect.width/7),0,(self.rect.width/7), self.rect.height),2)

        # black keys
        pygame.draw.rect(self.image, (0,0,0), (1*(self.rect.width/14),0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), (3*(self.rect.width/14),0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), (7*(self.rect.width/14),0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), (9*(self.rect.width/14),0,(self.rect.width/8), 3*self.rect.height/5),0)
        pygame.draw.rect(self.image, (0,0,0), (11*(self.rect.width/14),0,(self.rect.width/8), 3*self.rect.height/5),0)


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

    def drawme(self):
        self.image = pygame.Surface([300, 180])
        self.image.fill((250,250,250))
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

    staff_position = (20 + notename.rect.width/2 - staff.rect.width/2,20)
    keyboard_position = (20 + 20 + notename.rect.width, 20 + staff.rect.height/2 - keyboard.rect.height/2)
    notename_position = (20,staff.rect.height + 40)

    screen.blit(background, (0,0))
    screen.blit(background_green, (0,0))
    screen.blit(staff.image, staff_position)
    screen.blit(keyboard.image, keyboard_position)
    screen.blit(notename.image, notename_position)

    pygame.display.flip()

    current_notes = []
    i = 0
    changed = 0
    failure = 0


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

        staff.update()
        keyboard.update()
        notename.update()
        screen.blit(background, (0,0))
        if failure == 1:
            background_red.set_alpha(255*changed/CHANGE_LOOPS)
            screen.blit(background_red, (0,0))
        else:    
            background_green.set_alpha(255*changed/CHANGE_LOOPS)
            screen.blit(background_green, (0,0))

        screen.blit(staff.image, staff_position)
        screen.blit(keyboard.image, keyboard_position)
        screen.blit(notename.image, (20,staff.rect.height + 40))

        pygame.display.flip()

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
                    else:
                        changed = CHANGE_LOOPS
                        failure = 1



if __name__ == "__main__":
    main()