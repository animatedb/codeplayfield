import os
import enum
import math
from operator import *
import pygame as pg
from typing import List, Optional, Tuple, Union
import LibGame.Game2dBase as base2d
import LibGame.Game2dObject as object2d

def getDirection(xMove:int, yMove:int) -> int:
    """
    Gets a rotation angle for x and y movements.
    0 degrees = up, 90 degrees = right, 180 degrees = down, 270 degrees = left.
    """
    assert isinstance(xMove, (int, float)), 'xMove must be a number'
    assert isinstance(yMove, (int, float)), 'yMove must be a number'
    return math.atan2(yMove, xMove) * 180/3.14 + 90

class Rule:
    """
    Defines the base class for any rules. Most rules operate on
    objects, so this provides a way that the objects can initialize
    rules when the rules are added to the objects.
    Every class derived from Rule must have an update() method.
    """
    # In the future, this may have a condition object and action objects.
    def __init__(self, obj:Optional[object2d.Object]=None):
        self.obj = obj

    def setObject(self, obj:object2d.Object):
        """
        This is called by addRule or replaceRules when the rule is added
        to a game.
        """
        self.obj = obj

    def updateCheck(self):
        """ This makes sure that setObject was called before update() """
        assert self.obj != None, 'setObject must be called for ' + str(self)


class RuleMoveLinear(Rule):
    """ Moves an object image at a constant speed. """

    def __init__(self, xMove:int, yMove:int):
        """
        Initializes the rule.

        xMove: Moves the X amount. A positive number moves right.
               A negative number moves left. A larger value moves faster.

        xMove: Moves the Y amount. A positive number moves down.
               A negative number moves up. A larger value moves faster.
        """
        Rule.__init__(self)
        self.move = (xMove, yMove)

    def update(self):
        """
        Moves the object image.

        Moves the X and Y movement amount each time the Game2d.update()
        is called. This is a relative movement from the current position of
        the object.
        """
        self.updateCheck()
        self.obj.rect = self.obj.rect.move(self.move)

    def reverseX(self):
        """
        Reverses the X movement direction.

        This means that if the object was moving left, that this will cause
        future updates to move the object right.
        """
        self.move = (-self.move[0], self.move[1])

    def reverseY(self):
        """
        Reverses the Y movement direction.

        This means that if the object was moving up, that this will cause
        future updates to move the object down.
        """
        self.move = (self.move[0], -self.move[1])

    def reverseXAndRotateImage(self):
        self.reverseX()
        self.rotateToDirection()

    def reverseYAndRotateImage(self):
        self.reverseY()
        self.rotateToDirection()

    def rotateToDirection(self):
        if self.move[0] != 0 or self.move[1] != 0:
            if self.getDirection() != self.obj.getDirection():
                self.obj.rotateImage(self.getDirection())
                self.obj.setDirection(self.getDirection())

    def getDirection(self):
        return getDirection(self.move[0], self.move[1])

class RuleLimit(Rule):
    """ Runs an action when the limit is reached. """
    def __init__(self, objSide:base2d.ObjectSide, op, limit:int, actions:List):
        """
        Initializes the rule.

        objectSide: says which side of the object is checked.

        op: This can be gt (>), lt (<), eq (==), ne (!=), ge (>=), le (<=).
            If "import operator" was used, then "operator.gt" must be used.
            If "from operator import *" was used, then "gt" can be used.

        limit: Either an X or Y screen position.

        actions: The actions to run when the limit is reached. An action
            is a method or function with no parameters.
        """
        Rule.__init__(self)
        self.objSide = objSide
        self.op = op
        self.limit = limit
        for action in actions:
            assert action != None, 'Actions cannot be None'
        self.actions = actions

    """
    This checks the limit each time the Game2d.update() is called.
    If the limit is reached, this runs the actions.
    """
    def update(self):
        self.updateCheck()
        if self.op(self.obj.getSidePos(self.objSide), self.limit):
            for action in self.actions:
                action()

class RuleStopAnimation(Rule):
    """
    Stops the animation.

    obj: The object to stop the animation.

    The animation can be restarted by running rules like RuleMoveLeftRight.
    """
    def __init__(self):
        pass

    """ This stops the animation when Game2d.update() is called. """    
    def update(self):
        self.updateCheck()
        self.obj.runAnimation(False)


class RuleMoveLeftRightToLimits(Rule):
    """
    Moves an object between limits, then reverses direction and flips the image.

    speed: Moves the X amount. A positive number moves right.
           A negative number moves left. A larger value moves faster.

    leftLimit: The X screen position to change direction, and then move right.

    rightLimit: The X screen position the change direction, and then move left.
    """
    def __init__(self, speed:int=None, leftLimit:int = None, rightLimit:int=None):
        Rule.__init__(self)
        self.ruleMoveLinear = RuleMoveLinear(speed, 0)
        if not leftLimit:
            leftLimit = base2d.MainGame.getRect().left
        if not rightLimit:
            rightLimit = base2d.MainGame.getRect().right
        self.leftLimit = leftLimit
        self.rightLimit = rightLimit

    def setObject(self, obj:object2d.Object):
        super().setObject(obj)
        obj.runAnimation(True)
        actions = (self.ruleMoveLinear.reverseX, obj.flipX)
        self.ruleLimitRight = RuleLimit(base2d.ObjectSide.Right, gt,
            self.rightLimit, actions)
        self.ruleLimitLeft = RuleLimit(base2d.ObjectSide.Left, lt,
            self.leftLimit, actions)
        self.ruleMoveLinear.setObject(obj)
        self.ruleLimitLeft.setObject(obj)
        self.ruleLimitRight.setObject(obj)

    """
    Checks the limit each time the Game2d.update() is called.
    If the limit is reached, this reverses direction and flips the image.
    """
    def update(self):
        self.updateCheck()
        self.ruleMoveLinear.update()
        self.ruleLimitRight.update()
        self.ruleLimitLeft.update()

class RuleMoveInArea(Rule):
    def __init__(self, speedX:int=None, speedY:int=None, leftLimit:int = None, rightLimit:int=None,
        topLimit:int=None, bottomLimit:int=None):
        Rule.__init__(self)
        self.ruleMoveLinear = RuleMoveLinear(speedX, speedY)
        if not leftLimit:
            leftLimit = base2d.MainGame.getRect().left
        if not rightLimit:
            rightLimit = base2d.MainGame.getRect().right
        if not topLimit:
            topLimit = base2d.MainGame.getRect().top
        if not bottomLimit:
            bottomLimit = base2d.MainGame.getRect().bottom
        self.leftLimit = leftLimit
        self.rightLimit = rightLimit
        self.topLimit = topLimit
        self.bottomLimit = bottomLimit

    def setObject(self, obj:object2d.Object):
        obj.runAnimation(True)
        super().setObject(obj)
        self.ruleMoveLinear.setObject(obj)
        self.ruleMoveLinear.rotateToDirection()
        xActions = (self.ruleMoveLinear.reverseXAndRotateImage, )
        yActions = (self.ruleMoveLinear.reverseYAndRotateImage, )
        self.ruleLimitRight = RuleLimit(base2d.ObjectSide.Right, gt,
            self.rightLimit, xActions)
        self.ruleLimitLeft = RuleLimit(base2d.ObjectSide.Left, lt,
            self.leftLimit, xActions)
        self.ruleLimitTop = RuleLimit(base2d.ObjectSide.Top, lt,
            self.topLimit, yActions)
        self.ruleLimitBottom = RuleLimit(base2d.ObjectSide.Bottom, gt,
            self.bottomLimit, yActions)
        self.ruleLimitLeft.setObject(obj)
        self.ruleLimitRight.setObject(obj)
        self.ruleLimitTop.setObject(obj)
        self.ruleLimitBottom.setObject(obj)

    """
    Checks the limit each time the Game2d.update() is called.
    If the limit is reached, this reverses direction and flips the image.
    """
    def update(self):
        self.updateCheck()
        self.ruleMoveLinear.update()
        self.ruleLimitRight.update()
        self.ruleLimitLeft.update()
        self.ruleLimitTop.update()
        self.ruleLimitBottom.update()

class RuleMoveLeftRight(Rule):
    """
    This moves left or right.

    obj: The object to move.

    xMove: Moves the X amount. A positive number moves right.
           A negative number moves left. A larger value moves faster.

    This has no limits, so will move off the screen.
    """
    def __init__(self, xMove):
        Rule.__init__(self)
        self.xMove = xMove

    def setObject(self, obj:object2d.Object):
        super().setObject(obj)
        obj.runAnimation(True)

    """
    Moves the X position each time Game2d.update() is called.
    """
    def update(self):
        self.updateCheck()
        xPos, yPos = self.obj.getPosition()
        self.obj.setPosition(xPos+self.xMove, yPos)

class RuleTouches(Rule):
    def __init__(self, objects:List, actions:List) -> None:
        Rule.__init__(self)
        self.objects = objects
        self.actions = actions

    def update(self) -> None:
        self.updateCheck()
        for obj in self.objects:
            if self.obj.getRect().colliderect(obj.getRect()):
                for action in self.actions:
                    action()
                break;
