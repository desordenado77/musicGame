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
        



def filesInFolder(mypath):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def main(file_name, song_file, device_id):

    keyArray = {}
    keyArray[pygame.K_a] = "c"
    keyArray[pygame.K_s] = "d"
    keyArray[pygame.K_d] = "e"
    keyArray[pygame.K_f] = "f"
    keyArray[pygame.K_g] = "g"
    keyArray[pygame.K_h] = "a"
    keyArray[pygame.K_j] = "b"

    midiArray = {}
    midiArray[0] = "c"
    midiArray[2] = "d"
    midiArray[4] = "e"
    midiArray[5] = "f"
    midiArray[7] = "g"
    midiArray[9] = "a"
    midiArray[11] = "b"


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

    data = {}

    data["Song"] = song_file
    data["steps"] = []

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()
    playingMusic = 0
    pygame.mixer.music.pause()

    screen = pygame.display.set_mode((100, 100))
    pygame.display.set_caption("Music Game Song Recorder")
    pygame.display.flip()


    notFinished = True 

    step = 0

    clock = pygame.time.Clock()

    print "press q to exit"

    while notFinished:
        for event in pygame.event.get():
            keyFound = 0

            if event.type in [pygame.midi.MIDIIN]:
                if event.status == 128:
                    # Key released
#                    try:
                    print "step: " + str(step) + " note: " + midiArray[event.data1%12]
                    step = step + 1
                    noteToAdd = {}
                    noteToAdd["notes"] = midiArray[event.data1%12] 
                    data["steps"].append(noteToAdd)
#                    except:
#                        print "not handled key"
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                try:
                    print "step: " + str(step) + " note: " + keyArray[event.key]
                    step = step + 1
                    data["steps"][step]["notes"] = keyArray[event.key]
                except:
                    if event.key == pygame.K_q:
                        notFinished = 0
                    elif event.key == pygame.K_m:
                        if playingMusic == 1:
                            pygame.mixer.music.pause()
                            playingMusic = 0
                        else:
                            pygame.mixer.music.unpause()
                            playingMusic = 1
                    else:
                        print "not handled key"

            if midiInput.poll():
                midi_events = midiInput.read(10)
                # convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, midiInput.device_id)

                for m_e in midi_evs:
                    event_post( m_e )

        clock.tick(60)
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    try:
        file_name = str(sys.argv[1])
        song_file = str(sys.argv[2])
    except:
        print "usage:"
        print "\t" + sys.argv[0] + " json song_file [midi_device]"
        sys.exit(0)

    try:
        device_id = int( sys.argv[-1] )
    except:
        device_id = None

    main(file_name, song_file, device_id)