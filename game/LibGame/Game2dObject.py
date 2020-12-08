import os
import enum
from operator import *
import pygame as pg
import pygame.freetype
from typing import List, Optional, Tuple, Union
import LibGame.Game2dBase as base2d

if not pg.font:
    print('Warning, fonts disabled')
if not pg.mixer:
    print('Warning, sound disabled')


class Object(pg.sprite.Sprite):
    def __init__(self, filePattern:Union[List, str]):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        # This must be kept becase rotate and resize are are lossy.
        self.origImages = []
        self.images = []
        if isinstance(filePattern, str):
            if os.path.isdir(filePattern):
                filenames = [base2d.Path(filePattern, f) for f in os.listdir(filePattern)]
            else:
                filenames = [filePattern]
        else:
            filenames = filePattern
        for filepath in filenames:
            image = base2d.LoadImage(filepath)
            self.images.append(image)
            self.origImages.append(image.copy())
        self.setPosition(0, 0) # Default to known position
        self.direction = 0
        self.initialRotation = 0
        self.imageRotation = 0
        self.imageSize = base2d.MainGame.getSize()        # For default size.
        self.imageIndex = 0
        self.animationIncrement = 1
        self.rules = []
        self.rect = self.images[0].get_rect()

    def getRect(self):
        return self.rect

    def getSidePos(self, objSide:base2d.ObjectSide):
        if objSide == base2d.ObjectSide.Left:
            pos = self.rect.left
        elif objSide == base2d.ObjectSide.Right:
            pos = self.rect.right
        elif objSide == base2d.ObjectSide.Top:
            pos = self.rect.top
        else:
            pos = self.rect.bottom
        return pos

    def getSize(self):
        return self.rect.right, self.rect.bottom

    def setPosition(self, x:int, y:int) -> None:
        for image in self.images:
            self.rect = image.get_rect().move((x, y))

    def getPosition(self):
        return self.rect.topleft

    def rotateImageInitial(self, initialAngle) -> None:
        self.initialRotation = initialAngle        

    def rotateImage(self, angle:int) -> None:
        """
        Rotates the image relative to the last position.

        This does a clockwise rotation.
        """
        self.imageRotation = angle
        self._setSizeOrRotation()

    def setSize(self, x_or_size, y:int=None) -> None:
        if y:
            self.imageSize = (x_or_size, y)
        else:
            self.imageSize = x_or_size
        self._setSizeOrRotation()

    # Each time the size or rotation is changed, some pixels can be lost. So a
    # copy of the original image is stored, and the transforms are applied
    # on the original image instead of on the previously rotated or sized image.
    def _setSizeOrRotation(self) -> None:
        for index in range(0, len(self.images)):
            self.images[index] = pg.transform.rotate(self.origImages[index],
                -self.imageRotation+self.initialRotation)
        for index in range(0, len(self.images)):
            self.images[index] = pg.transform.scale(self.images[index], self.imageSize)

    # Direction is saved in the object because the direction must be sometime known
    # even if the object isn't moving.
    # Setting direction does not change the image because sometimes it should be a
    # flip and other times it should be a rotate (flip x and y).
    def setDirection(self, direction:int) -> None:
        """
        Sets the direction on the screen.

        direction: 0 is up, 90 is right, 180 is down, 180+90 (270) is left.

        This only stores a direction. It does not affect the image. It can be used
        to indicate an image to draw, or which direction the object will move.
        """
        self.direction = direction

    def getDirection(self) -> int:
        """
        Gets the direction on the screen.
        """
        return self.direction

    def addRule(self, rule):
        rule.setObject(self)
        self.rules.append(rule)

    def replaceRules(self, rules):
        for rule in rules:
            rule.setObject(self)
        self.rules = rules

    def update(self):
        self.imageIndex += self.animationIncrement
        if self.imageIndex >= len(self.images):
             self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        for rule in self.rules:
            rule.update()

    # Can be used to initialize the index to different values,
    # or to reset to a known image index.
    def setAnimationIndex(self, index:int) -> None:
        self.animationIncrement = index
        
    def runAnimation(self, on=True):
        if on:
            self.animationIncrement = 1
        else:
            self.animationIncrement = 0
            self.imageIndex = 0     # Set to first image in animation when stopped.

    def flipX(self):
        for index in range(0, len(self.images)):
            self.images[index] = pg.transform.flip(self.images[index], 1, 0)

class ObjectSound:
    def __init__(self, filename:str) -> None:
        self.sound = base2d.LoadSound(filename)

    def play(self):
        self.sound.play()

class ObjectText:
    def __init__(self, size=12):
        self.font = pg.freetype.SysFont('Comic Sans MS', size)

    def drawText(self, screen, text:str, x:int, y:int):
        surface, rect = self.font.render(text, (0,0,0))
#        screen.images[0].fill((255,255,255))
        surface.fill((255,255,255))
        surface, rect = self.font.render(text, (0,0,0), (0xff,0xff,0xff))
        screen.images[0].blit(surface, (x, y))

class ObjectScore(ObjectText):
    def __init__(self, screen, x, y, fontSize=12):
        ObjectText.__init__(self, fontSize)
        self.x = x
        self.y = y
        self.score = 0
        self.screen = screen

    def add(self):
        self.score += 1
        self.drawText(self.screen, str(self.score), self.x, self.y)
