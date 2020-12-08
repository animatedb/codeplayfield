#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
from LibGame.Game2dBase import *
from LibGame.Game2d import *
from LibGame.Game2dObject import *
from LibGame.Game2dRule import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "airport-data")


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    gameSize = (1000, 600)
    game = Game2d('Scene', gameSize)

    backImage = Object(Path(data_dir, 'airport-1000x600.jpg'))
    backImage.setSize(gameSize)

    bird = Object(Path(data_dir, 'Bird'))
    # @todo - coordinates should be as percent of full size image?
    bird.setSize(40, 40)
    bird.setPosition(10, 150)
    bird.flipX()

    bird.addRule(RuleMoveLeftRightToLimits(9))

    game.addObjects((backImage, bird))

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

