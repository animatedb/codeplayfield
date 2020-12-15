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
    outsideDoorRectLeft = 100 * outsideXScale
    outsideDoorRectWidth = (110-100) * outsideXScale
    # Rect is left, top, width, height
    outsideDoorRect = pg.Rect(outsideDoorRectLeft, 0, outsideDoorRectWidth, 600)

    insideXScale = 1000/230
    insideStairsRect = pg.Rect(65*insideXScale, 0, (80-65)*insideXScale, 600)
    insideDoorRect = pg.Rect(27*insideXScale, 0, (58-27)*insideXScale, 600)

    # Shows: Use Left, Right, Up, s, g keys
    keyText = obj.Object(base.Path(data_dir, 'keytext-scene.png'))
    keyText.runRules([rule.SetPosition(10, 10), rule.SetSize(350, 13)])

    boy = obj.Object(base.Path(data_dir, 'Boy'))
    boy.setDirection(90)
    boy.runRules([rule.StopAnimation(), rule.SetPosition(10, 300), rule.SetSize(100, 300)])

    girl = obj.Object(base.Path(data_dir, 'Girl'))
    girl.setDirection(270)
    girl.runRules([rule.StopAnimation(), rule.SetPosition(500, 300), rule.SetSize(100, 300)])

    dollGame.addObjects([scenes, keyText, boy, girl])

    # Main Loop
    activeObject = girl
    going = True
    while going:
        # Handle Input Events
        for event in dollGame.getEvent():
            if dollGame.checkKeyDown(event, 'b'):
                activeObject = boy
            elif dollGame.checkKeyDown(event, 'g'):
                activeObject = girl

            if dollGame.checkKeyDown(event, pg.K_LEFT):
                setImageDirection(activeObject, pg.K_LEFT)
                activeObject.updateRules([rule.MoveLeftRight(-20)])
            elif dollGame.checkKeyDown(event, pg.K_RIGHT):
                setImageDirection(activeObject, pg.K_RIGHT)
                activeObject.updateRules([rule.MoveLeftRight(20)])
            elif dollGame.checkKeyUp(event, pg.K_LEFT) or dollGame.checkKeyUp(event, pg.K_RIGHT):
                activeObject.updateRules([rule.StopAnimation()])

            elif dollGame.checkKeyDown(event, pg.K_DOWN):
                activeObject.updateRules([rule.StopAnimation()])
                # Check if scene image index is 1, this means the inside house is displayed.
                if scenes.getImageIndex() == 1:
                    if activeObject.touchesRect(insideStairsRect):
                        x, y = activeObject.getPosition()
                        activeObject.setPosition(x, 300)
            elif dollGame.checkKeyDown(event, pg.K_UP):
                activeObject.updateRules([rule.StopAnimation()])
                # Check if scene image index is 0, this means the outside house is displayed.
                if scenes.getImageIndex() == 0:
                    if activeObject.touchesRect(outsideDoorRect):
                        scenes.setImageIndex(1)
                # Check if scene image index is 1, this means the inside house is displayed.
                if scenes.getImageIndex() == 1:
                    if activeObject.touchesRect(insideDoorRect):
                        scenes.setImageIndex(0)
                        # If any object went outside, there is no second floor, so move all
                        # objects down.
                        x, y = girl.getPosition()
                        girl.setPosition(x, 300)
                        x, y = boy.getPosition()
                        boy.setPosition(x, 300)
                    elif activeObject.touchesRect(insideStairsRect):
                        x, y = activeObject.getPosition()
                        activeObject.setPosition(x, 0)
            elif dollGame.checkKeyUp(event, 'j') and activeObject == girl:
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

def setImageDirection(obj, keyDirection):
    if keyDirection == pg.K_RIGHT:
        direction = 90
    else:
        direction = 270
    if obj.getDirection() != direction:
        obj.flipX()
        obj.setDirection(direction)

# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

