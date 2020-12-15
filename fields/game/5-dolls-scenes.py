#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2d as game
import LibGame.Game2dBase as base
import LibGame.Game2dObject as obj
import LibGame.Game2dRule as rule

data_dir = "doll-data"

# Define some values for scenes.
# Sometimes enum is a better option. Especially for static type checking.
Outside = 0
Inside = 1

# Define some positions.
TopFloor = -5   # This is the top floor Y position of the tops of the movable objects.
BottomFloor = 300

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

    chair = obj.Object(base.Path(data_dir, 'chair.png'))
    chair.setPosition(1000, 125)     # Hide the chair by moving off screen
    chair.setSize(180, 170)
    chair.setLayer(1)   # The chair will be drawn on top of any lower layer object.
    chair.flipX()

    boy = obj.Object(base.Path(data_dir, 'Boy'))
    boy.setDirection(90)
    boy.runRules([rule.StopAnimation(), rule.SetPosition(10, BottomFloor),
        rule.SetSize(100, 300)])

    girl = obj.Object(base.Path(data_dir, 'Girl'))
    girl.setDirection(270)
    girl.runRules([rule.StopAnimation(), rule.SetPosition(500, BottomFloor),
        rule.SetSize(100, 300)])

    dollGame.addObjects([scenes, keyText, chair, boy, girl])

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
                if scenes.getImageIndex() == Inside:
                    if activeObject.touchesRect(insideStairsRect):
                        x, y = activeObject.getPosition()
                        activeObject.setPosition(x, BottomFloor)
            elif dollGame.checkKeyDown(event, pg.K_UP):
                activeObject.updateRules([rule.StopAnimation()])
                # Check if scene image index is 0, this means the outside house is displayed.
                if scenes.getImageIndex() == Outside:
                    chair.setPosition(1000, 125)     # Hide the chair by moving off screen
                    if activeObject.touchesRect(outsideDoorRect):
                        scenes.setImageIndex(Inside)
                # Check if scene image index is 1, this means the inside house is displayed.
                if scenes.getImageIndex() == Inside:
                    chair.setPosition(700, 129)  # Show the chair by moving on screen
                    if activeObject.touchesRect(insideDoorRect):
                        scenes.setImageIndex(Outside)
                        # If any object went outside, there is no second floor, so move all
                        # objects down.
                        x, y = girl.getPosition()
                        girl.setPosition(x, BottomFloor)
                        x, y = boy.getPosition()
                        boy.setPosition(x, BottomFloor)
                    elif activeObject.touchesRect(insideStairsRect):
                        x, y = activeObject.getPosition()
                        activeObject.setPosition(x, TopFloor)
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

