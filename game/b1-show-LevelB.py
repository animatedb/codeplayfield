#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2dBase as base2d
import LibGame.Game2d as game2d
import LibGame.Game2dObject as object2d

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "airport-data")


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    # @todo - this should probably set size from background image?
    game = game2d.Game2d('Scene', (1000, 600))

    backImage = object2d.Object(base2d.Path(data_dir, 'airport-1000x600.jpg'))
    backImage.setSize(1000, 600)

    bird = object2d.Object(base2d.Path(data_dir, 'Bird'))
    # @todo - coordinates should be as percent of full size image?
    bird.setSize(40, 40)
    bird.setPosition(10, 150)
    bird.flipX()
# THIS CODE IS NOT SUPPPORTED CURRENTLY
    ruleMoveLinear = game2d.RuleMoveLinear(9, 0)
    bird.addRule(ruleMoveLinear)

# python passing expressions to functions
# python delay expression
# python postponed evaluation of expression

#https://stackoverflow.com/questions/1185199/passing-expressions-to-functions
# Use eq from operator module
    # This doesn't work because the bird value must be retrieved later.
    bird.addRule(game2d.CheckX(gt, backImage.getArea()),
        (bird.flipX, ruleMoveLinear.reverseX))

    revRightRule = game2d.Rule()
    revRightRule.setCondition(game2d.ObjPosGt, backImage.getArea().right)
    revRightRule.setActions((bird.flipX, ruleMoveLinear.reverseX))
    bird.addRule(revRightRule)

    revLeftRule = game2d.Rule()
    revLeftRule.setCondition(game2d.ObjPosLt, backImage.getArea().left)
    revLeftRule.setActions((bird.flipX, ruleMoveLinear.reverseX))
    bird.addRule(revLeftRule)

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

