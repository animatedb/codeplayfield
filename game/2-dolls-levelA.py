#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2d as game2d
import LibGame.Game2dBase as base2d
import LibGame.Game2dObject as object2d
import LibGame.Game2dRule as rule2d

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "doll-data")


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    gameSize = (1000, 600)
    game = game2d.Game2d('Scene', gameSize)

    house = object2d.Object(base2d.Path(data_dir, 'House'))
    house.setSize(gameSize)
    # Shows: Use Left, Right, Up, s, g keys
    keyText = object2d.Object(base2d.Path(data_dir, 'keytext.png'))
    keyText.setPosition(20, 20)
    keyText.setSize(600, 40)

    boy = object2d.Object(base2d.Path(data_dir, 'Boy'))
    # @todo - coordinates should be as percent of full size image?
    boy.setSize(150, 400)
    boy.setPosition(10, 200)

    girl = object2d.Object(base2d.Path(data_dir, 'Girl'))
    girl.setSize(150, 400)
    girl.setPosition(500, 200)

    boy.addRule(rule2d.RuleMoveLeftRight(20))
    girl.addRule(rule2d.RuleMoveLeftRight(-20))

    game.addObjects((house, keyText, boy, girl))

    # Main Loop
    going = True
    while going:
        # Handle Input Events
        for event in game.getEvent():
            if game.checkKeyDown(event, 's'):
                boy.replaceRules((rule2d.RuleStopAnimation(),))
            elif game.checkKeyDown(event, 'g'):
                boy.replaceRules((rule2d.RuleMoveLeftRightToLimits(20),))
                # This has to be done since direction is not restored
                # Add stop to rule?
                boy.setPosition(10, 200)
            elif game.checkKeyDown(event, pg.K_LEFT):
                girl.replaceRules((rule2d.RuleMoveLeftRight(-20),))
            elif game.checkKeyDown(event, pg.K_RIGHT):
                girl.replaceRules((rule2d.RuleMoveLeftRight(20),))
            elif game.checkKeyUp(event, pg.K_LEFT) or game.checkKeyUp(event, pg.K_RIGHT):
                girl.replaceRules((rule2d.RuleStopAnimation(),))
            elif game.checkKeyUp(event, pg.K_UP) or game.checkKeyUp(event, pg.K_DOWN):
                girl.replaceRules((rule2d.RuleStopAnimation(),))

            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        game.update(5)
    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

