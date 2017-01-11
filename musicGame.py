#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import pygame.midi
from pygame.locals import *
import sys
import os
import json
import random
import time

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CHANGE_LOOPS = 4
BG_FOLDER = "./backgrounds"
MASCOT_SCALE = 0.40
MASCOT_SPEED = 2
ROCKET_SCALE = 0.4



def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))
        



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
    key = "g"

    def drawme(self):
        self.image.fill((250,250,250))
        if self.key == "f":
            self.image.blit(self.keyoff, (0, 35))
        else:
            self.image.blit(self.keyofg, (0, 0))

        self.rect = self.image.get_rect()
        i =0
        for i in range(1,6):
            pygame.draw.line(self.image, (0,0,0), (0, i*self.rect.height/7),(self.rect.width, i*self.rect.height/7),2)

#        pygame.draw.rect(self.image, (255,0,0), (0,0,self.rect.width, self.rect.height),2)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.keyoff = load_image("keyoff.png", "./", alpha=False, scale=0.18)
        self.keyofg = load_image("keyofg.png", "./", alpha=False)
        self.keyofg = pygame.transform.scale(self.keyofg, (80, 240))
        self.size = (80,240) 

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
            if self.key == "f":
                posy = posy - 5*self.rect.height/14
            else:
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

class Rocket(pygame.sprite.Sprite):
    position = (0,0)
    launchPosition = (0,0)
    launchStep = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rocketImage = load_image("rocket.png", "./rocket", alpha=True, scale=ROCKET_SCALE)
        self.size = self.rocketImage.get_size();
        self.image = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.blit(self.rocketImage, (0,0))

    def launch(self):
        if self.launchStep == 0:
            self.launchPosition = self.position
        if self.launchStep < 100:
            self.position = (self.launchPosition[0] + random.randint(1, 10), self.launchPosition[1] + random.randint(1, 10))
        if self.launchStep >= 100:
            self.position = (self.launchPosition[0], self.launchPosition[1] - (self.launchStep - 100)*4)
        
        if self.position[1] > -self.rect.height:
            self.launchStep = self.launchStep + 1
            return 0
        else:
            return 1

    def update(self):
        self.image.blit(self.rocketImage, (0,0))

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

    def hide(self):
        if self.position[0] >= self.targetPosition[0]:
            self.state = 3

        return self.state

    def moveTo(self, x, y):
        if ((self.position[0] != self.targetPosition[0]) or (self.position[1] != self.targetPosition[1])) and (self.state == 0):
            self.run()
        self.targetPosition = (x, y)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.idleImage.append(load_image("frame-1.png", "./idle", alpha=True, scale=MASCOT_SCALE))
        self.idleImage.append(load_image("frame-2.png", "./idle", alpha=True, scale=MASCOT_SCALE))
        self.idleImage.append(load_image("frame-1.png", "./idle", alpha=True, scale=MASCOT_SCALE))
        self.idleImage.append(load_image("frame-2.png", "./idle", alpha=True, scale=MASCOT_SCALE))
        self.runImage.append(load_image("frame-1.png", "./run", alpha=True, scale=MASCOT_SCALE))
        self.runImage.append(load_image("frame-2.png", "./run", alpha=True, scale=MASCOT_SCALE))
        self.runImage.append(load_image("frame-3.png", "./run", alpha=True, scale=MASCOT_SCALE))
        self.runImage.append(load_image("frame-4.png", "./run", alpha=True, scale=MASCOT_SCALE))
        self.dizzyImage.append(load_image("frame-1.png", "./dizzy", alpha=True, scale=MASCOT_SCALE))
        self.dizzyImage.append(load_image("frame-2.png", "./dizzy", alpha=True, scale=MASCOT_SCALE))
        self.dizzyImage.append(load_image("frame-1.png", "./dizzy", alpha=True, scale=MASCOT_SCALE))
        self.dizzyImage.append(load_image("frame-2.png", "./dizzy", alpha=True, scale=MASCOT_SCALE))
        self.state = 0 # idle
        # self.state = 1 # run
        self.step = 0
        self.image = pygame.Surface(self.idleImage[0].get_size(), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
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
                self.position = (min(self.targetPosition[0], self.position[0] + MASCOT_SPEED), self.position[1])

            if self.position[1] < self.targetPosition[1]:
                self.position = (self.position[0], self.position[1] + MASCOT_SPEED)

            if self.position[1] > self.targetPosition[1]:
                self.position = (self.position[0], self.position[1] - MASCOT_SPEED)

            if (self.position[0] == self.targetPosition[0]) and (self.position[1] == self.targetPosition[1]) and (self.state != 0):
                self.idle()


def filesInFolder(mypath):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def main(file_name, device_id):

    keyArray = {}
    keyArray["c"] = pygame.K_a
    keyArray["d"] = pygame.K_s
    keyArray["e"] = pygame.K_d
    keyArray["f"] = pygame.K_f
    keyArray["g"] = pygame.K_g
    keyArray["a"] = pygame.K_h
    keyArray["b"] = pygame.K_j

    midiArray = {}
    midiArray["c"] = 0
    midiArray["d"] = 2
    midiArray["e"] = 4
    midiArray["f"] = 5
    midiArray["g"] = 7
    midiArray["a"] = 9
    midiArray["b"] = 11


    pygame.init()

    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print ("using input_id :%s:" % input_id)
    midiInput = pygame.midi.Input( input_id )

    with open(file_name) as data_file:    
        data = json.load(data_file)

    file = data["Song"]

    print "Song: " + file

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    playingMusic = 0
    pygame.mixer.music.pause()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Music Game")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    
    bg_selected = random.choice(filesInFolder(BG_FOLDER))
    background_image = load_image(bg_selected, BG_FOLDER, alpha=False)
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
    rocket = Rocket()

    staff.position = (20 + notename.rect.width/2 - staff.rect.width/2,20)

    try:
        staff.key = data["key"]
    except:
        staff.key = "g"

    keyboard.position = (20 + 20 + notename.rect.width, 20 + staff.rect.height/2 - keyboard.rect.height/2)
    notename.position = (20,staff.rect.height + 40)
    mascot.position = (20, 690-mascot.rect.height)
    rocket.position = (1004-rocket.rect.width, 690-rocket.rect.height)

    screen.blit(background, (0,0))
    screen.blit(background_green, (0,0))
    screen.blit(staff.image, staff.position)
    screen.blit(keyboard.image, keyboard.position)
    screen.blit(notename.image, notename.position)
    screen.blit(mascot.image, mascot.position)
    screen.blit(rocket.image, rocket.position)

    pygame.display.flip()

    current_notes = []
    i = 0
    changed = 0
    failure = 0

#    mascot.moveTo(900, 580)
    clock = pygame.time.Clock()
    #prevtime = 0
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

        mascot.moveTo(((1024-180)/len(data["steps"]))*i+20, mascot.position[1])
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

        if i >= len(data["steps"]):
            # fly... 
            if mascot.hide() == 3:
                if rocket.launch() == 1:
                    # game done
                    print "done"
                    font = pygame.font.Font('comic-andy/comic_andy.ttf', 160)
                    fontRender = font.render("Muy Bien!!!", True, (255,0,0))
                    screen.blit(fontRender, (300, 160))
                    pygame.display.flip()
                    time.sleep(4)                    

                    sys.exit()
        else:
            screen.blit(staff.image, staff.position)
            screen.blit(keyboard.image, keyboard.position)
            screen.blit(notename.image, notename.position)

        screen.blit(mascot.image, mascot.position)
        screen.blit(rocket.image, rocket.position)

        pygame.display.flip()

        if changed == 0:
            for event in pygame.event.get():
                keyFound = 0

                if event.type in [pygame.midi.MIDIIN]:
                    if event.status == 128:
                        # Key released
                        for theNote in current_notes:
                            if (event.data1%12) == midiArray[theNote]:
                                i = i + 1
                                changed = CHANGE_LOOPS
                                failure = 0                        
                                keyFound = 1
                        if keyFound == 0:
                            changed = CHANGE_LOOPS
                            failure = 1
                            mascot.dizzy()

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
                        elif event.key == pygame.K_m:
                            if playingMusic == 1:
                                pygame.mixer.music.pause()
                                playingMusic = 0
                            else:
                                pygame.mixer.music.unpause()
                                playingMusic = 1
                        else:
                            changed = CHANGE_LOOPS
                            failure = 1
                            mascot.dizzy()

        if midiInput.poll():
            midi_events = midiInput.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, midiInput.device_id)

            for m_e in midi_evs:
                event_post( m_e )

        #curtime = pygame.time.get_ticks()
        clock.tick(60)
        #print "elapsed time " + str(curtime-prevtime)
        #prevtime = curtime


if __name__ == "__main__":

    try:
        file_name = str(sys.argv[1])
    except:
        print "usage:"
        print "\t" + sys.argv[0] + " json [midi_device]"
        sys.exit(0)        

    try:
        device_id = int( sys.argv[-1] )
    except:
        device_id = None

    main(file_name, device_id)