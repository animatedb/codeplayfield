#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2d as game
import LibGame.Game2dBase as base
import LibGame.Game2dObject as obj
import LibGame.Game2dRule as rule

data_dir = "doll-data"


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    gameSize = (1000, 600)
    dollGame = game.Game2d('Dolls', gameSize)

    house = obj.Object(base.Path(data_dir, 'House/house.jpg'))
    # runRules runs the rules right away.
    house.runRules([rule.SetSize(gameSize)])

    # Shows: Use Left, Right, Up, s, g keys
    keyText = obj.Object(base.Path(data_dir, 'keytext.png'))
    keyText.runRules([rule.SetPosition(20, 20), rule.SetSize(600, 40)])

    boy = obj.Object(base.Path(data_dir, 'Boy'))
    boy.runRules([rule.SetPosition(10, 200), rule.SetSize(150, 400)])

    girl = obj.Object(base.Path(data_dir, 'Girl'))
    girl.runRules([rule.SetPosition(500, 200), rule.SetSize(150, 400)])

    dollGame.addObjects([house, keyText, boy, girl])

    # updateRules adds the rules to the objects and the game runs the
    # rules every time the dollGame.update is called below.
    girl.updateRules([rule.MoveLeftRight(-20)])
    boy.updateRules([rule.MoveLeftRight(20)])

    # Main Loop
    going = True
    while going:
        # Handle Input Events
        for event in dollGame.getEvent():
            # Check if the 's' key was pressed.
            if dollGame.checkKeyDown(event, 's'):
                # The 's' key was pressed, so stop to only show a single image.
                # This also replaces RuleMoveLeftRight, so there is no movement anymore.
                boy.updateRules([rule.StopAnimation()])
            elif dollGame.checkKeyDown(event, 'g'):
                boy.updateRules([rule.MoveLeftRightToLimits(20)])
                # This has to be done since direction is not restored
                # Add stop to rule?
                boy.setPosition(10, 200)
            elif dollGame.checkKeyDown(event, pg.K_LEFT):
                girl.updateRules([rule.MoveLeftRight(-20)])
            elif dollGame.checkKeyDown(event, pg.K_RIGHT):
                girl.updateRules([rule.MoveLeftRight(20)])
            elif dollGame.checkKeyUp(event, pg.K_LEFT) or dollGame.checkKeyUp(event, pg.K_RIGHT):
                girl.updateRules([rule.StopAnimation()])
            elif dollGame.checkKeyUp(event, pg.K_DOWN) or dollGame.checkKeyUp(event, pg.K_UP):
                girl.updateRules([rule.StopAnimation()])

            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        dollGame.update(5)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

