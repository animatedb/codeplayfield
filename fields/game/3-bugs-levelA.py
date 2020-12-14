#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2d as game
import LibGame.Game2dBase as base
import LibGame.Game2dObject as obj
import LibGame.Game2dRule as rule

data_dir = "bug-data"


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    gameSize = (1000, 600)
    bugGame = game.Game2d('Scene', gameSize)

    objects = []
    spiders = []

    background = obj.Object(base.Path(data_dir, 'background.jpg'))
    background.setSize(gameSize)
    objects.append(background)
    score = obj.ObjectScore(background, 20, 20, 25)
    beep = obj.ObjectSound(base.Path(data_dir, 'beep.wav'))

    for i in range(0, 40):
        spider = obj.Object(base.Path(data_dir, 'Spider'))
        # @todo - coordinates should be as percent of full size image?
        spider.setSize(80, 80)
        # Initialize the rotation. The original image faces left, so make
        # it face up.
        spider.rotateImageInitial(360-120)
        spider.setPosition(base.Random(10, 800), base.Random(10, 500))
        spider.setAnimationIndex(base.Random(0, 6))
        spider.updateRules([rule.MoveInArea(base.Random(-5, 5),
            base.Random(-5, 5))])
        objects.append(spider)
        spiders.append(spider)

    bug = obj.Object(base.Path(data_dir, 'Bug'))
    bug.setSize(50, 50)
    bug.setPosition(200, 200)
    bug.updateRules([rule.TouchesObjects(spiders, (score.add, beep.play) )])
    objects.append(bug)

    bugGame.addObjects(objects)

    # Main Loop
    going = True
    x = 0
    y = 0
    lastx = 0
    lasty = 0
    while going:
        # Handle Input Events
        for event in bugGame.getEvent():
            if bugGame.checkKeyDown(event, pg.K_LEFT):
                x = -20
            elif bugGame.checkKeyDown(event, pg.K_RIGHT):
                x = 20
            elif bugGame.checkKeyDown(event, pg.K_UP):
                y = -20
            elif bugGame.checkKeyDown(event, pg.K_DOWN):
                y = 20
            elif bugGame.checkKeyUp(event, pg.K_LEFT):
                x = 0
            elif bugGame.checkKeyUp(event, pg.K_RIGHT):
                x = 0
            elif bugGame.checkKeyUp(event, pg.K_UP):
                y = 0
            elif bugGame.checkKeyUp(event, pg.K_DOWN):
                y = 0
            if lastx != x or lasty != y:
                bug.updateRules((rule.MoveInArea(x, y),
                    rule.TouchesObjects(spiders, (score.add, beep.play) )))
                lastx = x
                lasty = y

            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        bugGame.update(10)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

