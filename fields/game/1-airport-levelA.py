#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
from LibGame.Game2dBase import *
from LibGame.Game2d import *
from LibGame.Game2dObject import *
from LibGame.Game2dRule import *

data_dir = "airport-data"


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    gameSize = (1000, 600)
    game = Game2d('Scene', gameSize)

    airport = Object(Path(data_dir, 'airport-1000x600.jpg'))
    # runRules runs the rules right away.
    airport.runRules([SetSize(gameSize)])

    bird = Object(Path(data_dir, 'Bird'))
    bird.runRules([SetPosition(10, 150), SetSize(40, 40), FlipX()])

    game.addObjects([airport, bird])

    # updateRules runs the rules every time the dollGame.update is called below.
    bird.updateRules([MoveLeftRightToLimits(9)])

    # Main Loop
    going = True
    while going:
        # Handle Input Events
        for event in game.getEvent():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        game.update(15)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

