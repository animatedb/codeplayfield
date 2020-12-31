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

    # Make the screen size a width of 1000 and height of 600.
    gameSize = (1000, 600)
    game = Game2d('Scene', gameSize)

    # Initialize an object with an airport image.
    airport = Object(Path(data_dir, 'airport-1000x600.jpg'))
    # Set the size of the airport to be the full size of the game.
    # runRules runs the rules right away.
    airport.runRules([SetSize(gameSize)])

    # Initialize an object with images from the Bird folder.
    bird = Object(Path(data_dir, 'Bird'))
    # Set the initial position of the bird to X=10 and Y=150.
    # Set the size of the bird to a width of 40 and height of 40.
    # The bird images face left, so flip them horizontally so that
    # they face to the right.
    bird.runRules([SetPosition(10, 150), SetSize(40, 40), FlipX()])

    # Add the objects to the game so that the game can control the
    # rules and drawing.
    game.addObjects([airport, bird])

    # Add a rule to the bird so that it will start to move at a
    # steady pace, and will reverse when it reaches the limits of the screen.
    # updateRules runs the rules every time the dollGame.update is called below.
    bird.updateRules([MoveLeftRightToLimits(9)])

    # Main Loop
    going = True
    while going:
        # Handle Input Events
        for event in game.getEvent():
            # If the screen was closed, set the "going" variable to false
            # to quit the loop.
            if event.type == pg.QUIT:
                going = False
            # If the "Esc" key was pressed,  set the "going" variable to false
            # to quit the loop.
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        game.update(15)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

