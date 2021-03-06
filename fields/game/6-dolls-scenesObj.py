#!/usr/bin/env python

# Import Modules
import os
import pygame as pg
import LibGame.Game2d as game
import LibGame.Game2dBase as base
import LibGame.Game2dObject as obj
import LibGame.Game2dRule as rule
import LibGame.Game2dScenes as scenes

data_dir = "doll-data"

# Define some positions.
TopFloor = -5   # This is the top floor Y position of the tops of the movable objects.
NormalPlayerHeight = 300
BottomFloor = 300

GameSize = (1000, 600)

class DollGame(game.Game2d):
    def __init__(self):
        game.Game2d.__init__(self, 'Scene', GameSize)

        # Shows: Use Left, Right, Up, s, g keys
        self.keyText = obj.Object(base.Path(data_dir, 'keytext-scene.png'))
        self.keyText.setLayer(1)
        self.keyText.runRules([rule.SetPosition(10, 10), rule.SetSize(350, 13)])

        self.boy = obj.Object(base.Path(data_dir, 'Boy'))
        self.boy.setLayer(1)
        self.boy.setAnimationSpeed(3)
        self.boy.setDirection(90)
        self.boy.runRules([rule.StopAnimation(), rule.SetPosition(100, BottomFloor),
            rule.SetSize(100, 300)])

        self.girl = obj.Object(base.Path(data_dir, 'Girl'))
        self.girl.setLayer(1)
        self.girl.setAnimationSpeed(3)
        self.girl.setDirection(270)
        self.girl.runRules([rule.StopAnimation(), rule.SetPosition(500, BottomFloor),
            rule.SetSize(100, 300)])

        self.addObjects([self.keyText, self.boy, self.girl])
        self.activeObject = self.girl
        self.moveSpeed = 10

    def checkEvent(self, event):
        if self.checkKeyDown(event, 'b'):
            self.activeObject = self.boy
        elif self.checkKeyDown(event, 'g'):
            self.activeObject = self.girl

        elif self.checkKeyDown(event, pg.K_LEFT):
            setImageDirection(self.activeObject, pg.K_LEFT)
            self.activeObject.updateRules([rule.MoveLeftRight(-self.moveSpeed)])
        elif self.checkKeyDown(event, pg.K_RIGHT):
            setImageDirection(self.activeObject, pg.K_RIGHT)
            self.activeObject.updateRules([rule.MoveLeftRight(self.moveSpeed)])
        elif self.checkKeyUp(event, pg.K_LEFT) or self.checkKeyUp(event, pg.K_RIGHT):
            self.activeObject.updateRules([rule.StopAnimation()])

        elif self.checkKeyDown(event, pg.K_DOWN):
            self.activeObject.updateRules([rule.StopAnimation()])
        elif self.checkKeyDown(event, pg.K_UP):
            self.activeObject.updateRules([rule.StopAnimation()])
        elif self.checkKeyUp(event, 'j') and self.activeObject == self.girl:
            self.girl.runRules([rule.SetImages(base.Path(data_dir, 'Girl-Jump')),
                rule.SetSize(100, NormalPlayerHeight), rule.RunAnimation()])
            # These rules are run when the jump is finished.
            # Go back to left/right images.
            jumpDoneRules = [ rule.SetImages(base.Path(data_dir, 'Girl')),
                rule.SetSize(100, NormalPlayerHeight), rule.MoveLeftRight(0),
                rule.StopAnimation()
                ]
            rules = (rule.Jump(-40, 3, jumpDoneRules),)
            self.girl.updateRules(rules)
        elif dollGame.checkKeyDown(event, 'h') and self.activeObject == self.boy:
            self.activeObject.runRules([rule.PlaySound('doll-data/hello-1Kto3K.ogg')])


dollGame = DollGame()
sceneDirector = scenes.SceneDirector(dollGame)


# Top and bottom of doors and stairs don't really matter for this game, so just
# make them full height of screen.
# Use Gimp to get the image positions.
outsideXScale = 1000/235     # Scene X / image X
outsideDoorRectLeft = 100 * outsideXScale
outsideDoorRectWidth = (110-100) * outsideXScale
# Rect is left, top, width, height
outsideDoorRect = pg.Rect(outsideDoorRectLeft, 0, outsideDoorRectWidth, 600)
# Left side of scene
leftSideRect = pg.Rect(0, 0, 50, 600)
rightSideRect = pg.Rect(GameSize[0]-20, 0, 50, 600)

class HouseOutsideScene(scenes.Game2dScene):
    def __init__(self):
        scenes.Game2dScene.__init__(self, 'HouseOutside')
        house = self.addObject(base.Path(data_dir, 'House/house.jpg'))
        house.runRules([rule.SetSize(GameSize)])

    def checkEvent(self, event) -> None:
        if dollGame.checkKeyDown(event, pg.K_UP):
            if dollGame.activeObject.touchesRect(outsideDoorRect):
                sceneDirector.showScene('InsideDownstairs')
#        elif dollGame.checkKeyDown(event, pg.K_LEFT):
        else:   # Handle timer
            if dollGame.activeObject.touchesRect(leftSideRect):
                sceneDirector.showScene('City')

    def enterScene(self):
        scenes.Game2dScene.enterScene(self)
        # If any object went from inside to outside, there is no second floor,
        # so move all objects down.
        x, y = dollGame.girl.getPosition()
        dollGame.girl.setPosition(x, BottomFloor)
        x, y = dollGame.boy.getPosition()
        dollGame.boy.setPosition(x, BottomFloor)
        x, y = dollGame.activeObject.getPosition()
        dollGame.activeObject.runRules([rule.SetPosition(GameSize[0]*1/2, y)])

insideXScale = 1000/230
insideStairsRect = pg.Rect(65*insideXScale, 0, (80-65)*insideXScale, 600)
insideDoorRect = pg.Rect(27*insideXScale, 0, (58-27)*insideXScale, 600)

def addChair(scene):
    chair = scene.addObject(base.Path(data_dir, 'chair200x175.png'))
    chair.showImage(False)
    chair.setPosition(700, 129)
    chair.setSize(180, 170)
    chair.setLayer(2)   # The chair will be drawn on top of any lower layer object.
    chair.flipX()

def addDresser(scene):
    dresser = scene.addObject(base.Path(data_dir, 'dresser300x240.jpg'))
    dresser.showImage(False)
    dresser.setPosition(70, 123)
    dresser.setSize(180, 170)

class HouseInsideDownstairsScene(scenes.Game2dScene):
    def __init__(self):
        scenes.Game2dScene.__init__(self, 'InsideDownstairs')
        house = self.addObject(base.Path(data_dir, 'House/houseInside1.jpg'))
        house.runRules([rule.SetSize(GameSize)])
        chair = addChair(self)
        dresser = addDresser(self)

    def checkEvent(self, event) -> None:
        if dollGame.checkKeyDown(event, pg.K_UP):
            if dollGame.activeObject.touchesRect(insideDoorRect):
                sceneDirector.showScene('HouseOutside')
            elif dollGame.activeObject.touchesRect(insideStairsRect):
                sceneDirector.showScene('InsideUpstairs')
                x, y = dollGame.activeObject.getPosition()
                dollGame.activeObject.setPosition(x, TopFloor)

class HouseInsideUpstairsScene(scenes.Game2dScene):
    def __init__(self):
        scenes.Game2dScene.__init__(self, 'InsideUpstairs')
        house = self.addObject(base.Path(data_dir, 'House/houseInside1.jpg'))
        house.runRules([rule.SetSize(GameSize)])
        chair = addChair(self)
        dresser = addDresser(self)

    def checkEvent(self, event) -> None:
        if dollGame.checkKeyDown(event, pg.K_DOWN):
            if dollGame.activeObject.touchesRect(insideStairsRect):
                sceneDirector.showScene('InsideDownstairs')
                x, y = dollGame.activeObject.getPosition()
                dollGame.activeObject.setPosition(x, BottomFloor)

class AirportScene(scenes.Game2dScene):
    def __init__(self):
        scenes.Game2dScene.__init__(self, 'Airport')
        airport = self.addObject(base.Path('airport-data', 'airport-1000x600.jpg'))
        airport.runRules([rule.SetSize(GameSize)])
        child = self.addObject(base.Path(data_dir, 'BoyWalkingTransSmall.png'))
        child.setPosition(GameSize[0]*1/4, 400)

    def enterScene(self):
        scenes.Game2dScene.enterScene(self)
        dollGame.activeObject.runRules([rule.PlaySound('doll-data/trumpets.ogg')])
        x, y = dollGame.activeObject.getPosition()
        dollGame.activeObject.runRules([rule.SetPosition(GameSize[0]*1/2, y)])

    def checkEvent(self, event) -> None:
#        if dollGame.checkKeyDown(event, pg.K_RIGHT):
        # For any event like timer, check  the rectangle.
            if dollGame.activeObject.touchesRect(rightSideRect):
                sceneDirector.showScene('City')

class CityScene(scenes.Game2dScene):
    def __init__(self):
        scenes.Game2dScene.__init__(self, 'City')
        city = self.addObject(base.Path('city-data', 'city-1000x600.jpg'))
        city.runRules([rule.SetSize(GameSize)])
        cityFore = self.addObject(base.Path('city-data', 'city-1000x600-fore.png'))
        cityFore.runRules([rule.SetSize(GameSize)])
        cityFore.setLayer(2)
        self.car = self.addObject(base.Path('city-data', 'car.png'))
        self.car.runRules([rule.SetPosition(GameSize[0]*1/2, 280),
            rule.SetSize(int(600*.7), int(217*.7))])

    def enterScene(self):
        scenes.Game2dScene.enterScene(self)

        x, y = dollGame.activeObject.getPosition()
        dollGame.activeObject.runRules([rule.SetPosition(GameSize[0]*1/2, y)])
        self.savedActiveObject = dollGame.activeObject

        dollGame.boy.runRules([rule.SetSize(100, 200)])
        dollGame.girl.runRules([rule.SetSize(100, 200)])

    def leaveScene(self):
        scenes.Game2dScene.leaveScene(self)
        dollGame.girl.runRules([rule.SetSize(100, NormalPlayerHeight)])
        dollGame.boy.runRules([rule.SetSize(100, NormalPlayerHeight)])
        dollGame.activeObject = self.savedActiveObject

    def checkEvent(self, event) -> None:
        if dollGame.checkKeyDown(event, 'c'):
            dollGame.activeObject = self.car
        elif dollGame.activeObject != self.car:
            # For any event like timer, check  the rectangle.
            if dollGame.activeObject.touchesRect(rightSideRect):
                sceneDirector.showScene('HouseOutside')
            elif dollGame.activeObject.touchesRect(leftSideRect):
                sceneDirector.showScene('Airport')
            elif dollGame.activeObject == self.car:
                dollGame.moveSpped = 10
            else:
                dollGame.moveSpeed = 20


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    sceneDirector.addScenes([HouseOutsideScene(), HouseInsideDownstairsScene(),
        HouseInsideUpstairsScene(), CityScene(), AirportScene()])
    sceneDirector.showScene('HouseOutside')

    dollGame.addObjects(sceneDirector.getObjects())
    # Set a timer event for every 1/4 second. This allows checkEvent to be
    # called every once in a while.
    dollGame.setTimerEvent(250)

    # Main Loop
    going = True
    while going:
        # Handle Input Events
        for event in dollGame.getEvent():
            dollGame.checkEvent(event)
            sceneDirector.checkEvent(event)

            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
        dollGame.update(30)
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

