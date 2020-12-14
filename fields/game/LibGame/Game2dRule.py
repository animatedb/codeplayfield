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
    Many rules are postponed and are called from the game loop using update().
    Some rules are run using update() and others can be run immediately when
    Object.runRules() is called.

    endRule() is called when the rule is replaced. This can be used to restore the
        original state of the object.

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

    # @todo - remove concept of actions
    def checkActions(self):
        # @todo - should check whether it is callable.
        for action in self.actions:
            assert action != None, 'Actions cannot be None. The actions cannot be a function call with parenthesis'

    def updateCheckObject(self):
        """ This makes sure that setObject was called before update() """
        assert self.obj != None, 'setObject must be called for ' + str(self)

    def endRule(self, obj:object2d.Object):
        pass


class RuleMoveLinear(Rule):
    """ Moves an object image at a constant speed. """

    def __init__(self, xMove:int, yMove:int):
        """
        Initializes the rule.

        xMove: Moves the X amount. A positive number moves right.
               A negative number moves left. A larger value moves faster.

        yMove: Moves the Y amount. A positive number moves down.
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
        self.updateCheckObject()
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

# Moves in the up direction starting from the current object position
# slow, then faster, then slowing again.
# Then moves in the down direction with the same speed as up.
class RuleJump(Rule):
    def __init__(self, yMove:int, yIncrement:int, rules:List):
        """
        Initializes the rule.

        yMove: The total distance to move. A positive number moves down.
               A negative number moves up. A larger value moves faster.

        yIncrement: Should always be positive.
        """
        Rule.__init__(self)
        self.yMove = yMove
        if yMove > 0:
            self.ySpeed = yIncrement
        else:
            self.ySpeed = -yIncrement
        self.yIncrement = self.ySpeed
        self.objectEndY = None
        self.rules = rules

    def update(self):
        """
        Moves the object image.

        Moves the X and Y movement amount each time the Game2d.update()
        is called. This is a relative movement from the current position of
        the object.
        """
        self.updateCheckObject()
        if self.ySpeed != 0:    # Use zero to indicate jump is complete.
            # If starting a jump, set some target positions.
            objRect = self.obj.getRect()
            if self.objectEndY == None:
                self.startRect = objRect
                if self.ySpeed > 0:
                    self.objectEndY = self.obj.getRect().top - self.yMove
                    self.objectMidY = self.obj.getRect().top - self.yMove / 2
                else:
                    self.objectEndY = self.obj.getRect().top + self.yMove
                    self.objectMidY = self.obj.getRect().top + self.yMove / 2
            if self.ySpeed < 0:   # Going up?
                # Y Speed will go -1, -2, -3,..., -2, -1,...
                if objRect.top > self.objectMidY:  # While object is lower than mid target.
                    self.ySpeed += self.yIncrement    # Going up faster.
                else:
                    if self.ySpeed > self.yIncrement:     # Never let the speed go to 0.
                        self.ySpeed -= self.yIncrement    # Going up slower.
                    # If we reach the end, reverse direction
                    if objRect.top < self.objectEndY:
                        self.yIncrement = -self.yIncrement
                        self.ySpeed = self.yIncrement
            else:  # Going down
                # Y Speed will go 1, 2, 3,..., 2, 1,...
                if objRect.top < self.objectMidY:  # While object is higher than mid target.
                    self.ySpeed += self.yIncrement    # Go down faster.
                else:
                    if self.ySpeed > self.yIncrement:     # Never let the speed go to 0.
                        self.ySpeed -= self.yIncrement    # Going down slower.
                    # If we reach the end, done
                    if objRect.top > self.startRect.top:
                        # Done with jump
                        # Just reset to starting position.
                        self.objectEndY = None
                        self.ySpeed = 0
                        self.obj.rect = self.startRect
        if self.ySpeed != 0:
            moveAmount = (0, self.ySpeed)
            self.obj.rect = self.obj.rect.move(moveAmount)
        else:
            self.obj.runRules(self.rules)

    def endRule(self, obj):
        self.obj.rect = self.startRect

class RuleLimit(Rule):
    """ Runs an action when the limit is reached. """
# @todo - get rid of actions. See RuleJump
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
        self.actions = actions
        self.checkActions()

    """
    This checks the limit each time the Game2d.update() is called.
    If the limit is reached, this runs the actions.
    """
    def update(self):
        self.updateCheckObject()
        if self.op(self.obj.getSidePos(self.objSide), self.limit):
            for action in self.actions:
                action()

class RuleReplaceRules(Rule):
    def __init__(self, rules:List):
        self.rules = rules

    def update(self):
        self.obj.replaceRules(self.rules)

class RuleStopAnimation(Rule):
    """
    Stops the animation.

    The animation can be restarted by running rules like RuleMoveLeftRight.
    """
    def __init__(self):
        pass

    """ This stops the animation when Game2d.update() is called. """    
    def update(self):
        self.updateCheckObject()
        self.obj.stopAnimation()

class RuleSetImages(Rule):
    """
    Sets images.

    obj: The object to set images to.
    """
    def __init__(self, filePattern:Union[List, str]):
        self.filePattern = filePattern

    def update(self):
        self.updateCheckObject()
        self.obj.setImages(self.filePattern)

class RuleSetSize(Rule):
    """
    Sets image size.

    obj: The object to set size.
    """
    def __init__(self, xOrSize, y:int=None):
        self.xOrSize = xOrSize
        self.y = y

    def update(self):
        self.updateCheckObject()
        self.obj.setSize(self.xOrSize, self.y)

class RuleMoveLeftRightToLimits(Rule):
    """
    Moves an object between limits, then reverses direction and flips the image.

    speed: Moves a distance during the game loop. A positive number moves right.
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
        self.updateCheckObject()
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
        self.updateCheckObject()
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
        self.updateCheckObject()
        xPos, yPos = self.obj.getPosition()
        self.obj.setPosition(xPos+self.xMove, yPos)

class RuleTouches(Rule):
    def __init__(self, objects:List, actions:List) -> None:
        Rule.__init__(self)
        self.objects = objects
        self.actions = actions

    def update(self) -> None:
        self.updateCheckObject()
        for obj in self.objects:
            if self.obj.getRect().colliderect(obj.getRect()):
                for action in self.actions:
                    action()
                break;
