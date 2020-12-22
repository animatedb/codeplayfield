import os
import enum
from operator import *
import pygame as pg
from typing import List, Optional, Tuple, Union
import LibGame.Game2dBase as base2d

if not pg.font:
    print('Warning, fonts disabled')
if not pg.mixer:
    print('Warning, sound disabled')

class Game2d:
    def __init__(self, caption:str, size:Optional[Tuple[int, int]]=None):
        # Initialize Everything
        pg.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pg.init()
        if not size:
            size = (640, 480)
        self.rect = pg.Rect(0, 0, size[0], size[1])
        self.screen = pg.display.set_mode((size[0], size[1]))
        pg.display.set_caption(caption)
        pg.mouse.set_visible(0)

        # Create The Backgound
        self.background = pg.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250, 250, 250))

        # Display The Background
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()

        self.clock = pg.time.Clock()
        base2d.MainGame = self
        self.allObjects = pg.sprite.LayeredUpdates()

    def addObjects(self, objects):
        self.allObjects.add(objects)

    def update(self, clockTick:int):
        """ Runs rules for all objects that were added with addObjects """
        self.allObjects.update()

        # Clear the background surface
#        self.screen.blit(self.background, (0, 0))
        # LayeredUpdates.draw() calls pygame.Surface.surface.blit() for all self.sprites()
        # It returns a list of changed areas.
        # The problem is that there doesn't appear to be any way to prevent
        # drawing of some sprites.
#        self.allObjects.draw(self.screen)
        for obj in self.allObjects:
            if obj.showImages:
                self.screen.blit(obj.image, obj.rect)
        pg.display.flip()

        self.clock.tick(clockTick)

    def checkKeyDown(self, event, key):
        try:
            key = ord(key)
        except:
            pass
        return event.type == pg.KEYDOWN and event.key == key

    def checkKeyUp(self, event, key):
        try:
            key = ord(key)
        except:
            pass
        return event.type == pg.KEYUP and event.key == key

    def getRect(self):
        return self.rect

    def getSize(self):
        return self.rect.size

    def getEvent(self):
        return pg.event.get()

