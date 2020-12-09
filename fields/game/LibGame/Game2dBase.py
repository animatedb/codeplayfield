import enum
import os
import random
from operator import *
import pygame as pg
from typing import List, Optional, Tuple, Union

if not pg.font:
    print('Warning, fonts disabled')
if not pg.mixer:
    print('Warning, sound disabled')

MainGame = None

def Path(dirname:str, filename:str) -> str:
    """ Joins a directory and filename to create a full path to a file. """
    return os.path.join(dirname, filename)

def Random(start, stop):
    v = random.randint(start, stop)
    return v

# @todo - this must be called after Game2d because pg.image is there.
def LoadImage(filepath:str) -> pg.Surface:
    """ Loads an image from a file."""
    try:
        image = pg.image.load(filepath).convert_alpha()
    except:
        raise ValueError('Unable to load image: ' + str(filepath))
    return image

def LoadSound(filepath:str):
    """ Loads a sound from a file."""
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    try:
        sound = pg.mixer.Sound(filepath)
    except:
        raise ValueError('Unable to load sound: ' + str(filepath))
    return sound


class ObjectSide(enum.Enum):
    """ Describes a side of the object """
    Left = 1
    Right = 2
    Top = 3
    Bottom = 4
