#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2d as game2d
import LibGame.Game2dBase as base2d
import LibGame.Game2dObject as object2d
import LibGame.Game2dRule as rule2d

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "bug-data")


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    gameSize = (1000, 600)
    game = game2d.Game2d('Scene', gameSize)

    objects = []
    spiders = []

    background = object2d.Object(base2d.Path(data_dir, 'background.jpg'))
    background.setSize(gameSize)
    objects.append(background)
    score = object2d.ObjectScore(background, 20, 20, 25)
    beep = object2d.ObjectSound(base2d.Path(data_dir, 'beep.wav'))

    for i in range(0, 40):
        spider = object2d.Object(base2d.Path(data_dir, 'Spider'))
        # @todo - coordinates should be as percent of full size image?
        spider.setSize(80, 80)
        # Initialize the rotation. The original image faces left, so make
        # it face up.
        spider.rotateImageInitial(360-120)
        spider.setPosition(base2d.Random(10, 800), base2d.Random(10, 500))
        spider.setAnimationIndex(base2d.Random(0, 6))
        spider.addRule(rule2d.RuleMoveInArea(base2d.Random(-5, 5), base2d.Random(-5, 5)))
        objects.append(spider)
        spiders.append(spider)

    bug = object2d.Object(base2d.Path(data_dir, 'Bug'))
    bug.setSize(50, 50)
    bug.setPosition(200, 200)
    bug.addRule(rule2d.RuleTouches(spiders, (score.add, beep.play) ))
    objects.append(bug)

    game.addObjects(objects)

    # Main Loop
    going = True
    x = 0
    y = 0
    lastx = 0
    lasty = 0
    while going:
        # Handle Input Events
        for event in game.getEvent():
            if game.checkKeyDown(event, pg.K_LEFT):
                x = -20
            elif game.checkKeyDown(event, pg.K_RIGHT):
                x = 20
            elif game.checkKeyDown(event, pg.K_UP):
                y = -20
            elif game.checkKeyDown(event, pg.K_DOWN):
                y = 20
            elif game.checkKeyUp(event, pg.K_LEFT):
                x = 0
            elif game.checkKeyUp(event, pg.K_RIGHT):
                x = 0
            elif game.checkKeyUp(event, pg.K_UP):
                y = 0
            elif game.checkKeyUp(event, pg.K_DOWN):
                y = 0
            if lastx != x or lasty != y:
                bug.replaceRules((rule2d.RuleMoveInArea(x, y),
                    rule2d.RuleTouches(spiders, (score.add, beep.play) )))
                lastx = x
                lasty = y

            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        game.update(10)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

