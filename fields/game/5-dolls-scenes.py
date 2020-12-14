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
    dollGame = game.Game2d('Scene', gameSize)

    # First image is the outside of the house.
    scenes = obj.Object(base.Path(data_dir, 'House'))
    scenes.runRules([rule.StopAnimation(), rule.SetSize(gameSize)])

    # Top and bottom of doors and stairs don't really matter for this game, so just
    # make them full height of screen.
    # Use Gimp to get the image positions.
    outsideXScale = 1000/235     # Scene X / image X
    outsideDoorRectLeft = 95 * outsideXScale
    outsideDoorRectWidth = (115-94) * outsideXScale
    # Rect is left, top, width, height
    outsideDoorRect = pg.Rect(outsideDoorRectLeft, 0, outsideDoorRectWidth, 600)

    insideXScale = 1000/230
    insideStairsRect = pg.Rect(63*insideXScale, 0, (88-63)*insideXScale, 600)
    insideDoorRect = pg.Rect(27*insideXScale, 0, (58-27)*insideXScale, 600)

    # Shows: Use Left, Right, Up, s, g keys
    keyText = obj.Object(base.Path(data_dir, 'keytext.png'))
    keyText.runRules([rule.SetPosition(20, 20), rule.SetSize(600, 40)])

    boy = obj.Object(base.Path(data_dir, 'Boy'))
    boy.runRules([rule.SetPosition(10, 300), rule.SetSize(100, 300)])

    girl = obj.Object(base.Path(data_dir, 'Girl'))
    girl.runRules([rule.SetPosition(500, 300), rule.SetSize(100, 300)])

    dollGame.addObjects([scenes, keyText, boy, girl])

    # updateRules runs the rules every time the dollGame.update is called below.
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
            elif dollGame.checkKeyUp(event, pg.K_DOWN):
                girl.updateRules([rule.StopAnimation()])
                if scenes.getImageIndex() == 1 and girl.touchesRect(insideStairsRect):
                    x, y = girl.getPosition()
                    girl.setPosition(x, 300)
            elif dollGame.checkKeyUp(event, pg.K_UP):
                girl.updateRules([rule.StopAnimation()])
                if scenes.getImageIndex() == 0 and girl.touchesRect(outsideDoorRect):
                    scenes.setImageIndex(1)
                if scenes.getImageIndex() == 1:
                    if girl.touchesRect(insideDoorRect):
                        scenes.setImageIndex(0)
                    elif girl.touchesRect(insideStairsRect):
                        x, y = girl.getPosition()
                        girl.setPosition(x, 0)
            elif dollGame.checkKeyUp(event, 'j'):
                girl.runRules([rule.SetImages(base.Path(data_dir, 'Girl-Jump')),
                    rule.SetSize(150, 500), rule.RunAnimation()])
                # These rules are run when the jump is finished.
                # Go back to left/right images.
                jumpDoneRules = [ rule.SetImages(base.Path(data_dir, 'Girl')),
                    rule.SetSize(150, 400), rule.MoveLeftRight(0),
                    rule.StopAnimation()
                    ]
                rules = (rule.Jump(-40, 3, jumpDoneRules),)
                girl.updateRules(rules)

            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        dollGame.update(5)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

