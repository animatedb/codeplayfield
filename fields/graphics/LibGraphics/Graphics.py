from LibGraphics.graphics import *
from typing import Any, List, Optional

def CreateWindow(windowSizeX:int, windowSizeY:int, windowTitle:Optional[str]=None,
    backgroundColor:Optional[str]=None) -> GraphWin:
    if windowTitle == None:
        windowTitle = 'Window'
    window = GraphWin(windowTitle, windowSizeX, windowSizeY) # give title and dimensions
    if backgroundColor:
        window.setBackground(backgroundColor)
    # Set so that a bigger Y is lower on the screen, this is the default.
#    window.setCoords(0, windowSizeY, windowSizeX, 0)
    return window

def DrawPoint(window:GraphWin, point:Any) -> None:
    point.draw(window)

def DrawCircle(window:GraphWin, circleCenterX:int, circleCenterY:int, radius:int,
    fillColor:str, lineColor:str='black', width:int=1) -> Circle:
    circle = Circle(Point(circleCenterX, circleCenterY), radius) # set center and radius
    circle.setFill(fillColor)
    circle.setOutline(lineColor)
    circle.setWidth(width)
    circle.draw(window)
    return circle

def DrawRectangle(window:GraphWin, point1X:int, point1Y:int, point2X:int, point2Y:int,
    fillColor:str, lineColor:str='black', width:int=1):
    rect = Rectangle(Point(point1X, point1Y), Point(point2X, point2Y))
    rect.setFill(fillColor)
    rect.setOutline(lineColor)
    rect.setWidth(width)
    rect.draw(window)
    return rect

def DrawLine(window:GraphWin, point1X:int, point1Y:int, point2X:int, point2Y:int,
    fillColor:str, lineColor:str='black', width:int=1) -> Line:
    line = Line(Point(point1X, point1Y), Point(point2X, point2Y)) # set line points
    line.setFill(fillColor)
    line.setOutline(lineColor)
    line.setWidth(width)
    line.draw(window)
    return line

def DrawOval(window:GraphWin, point1X:int, point1Y:int, point2X:int, point2Y:int,
    fillColor:str, lineColor:str='black', width:int=1) -> Oval:
    oval = Oval(Point(point1X, point1Y), Point(point2X, point2Y)) # set corners of bounding box
    oval.setFill(fillColor)
    oval.setOutline(lineColor)
    oval.draw(window)
    return oval

def UpdateText(window, text:Text, textStr:str, size:Optional[int]=None,
    foregroundColor:Optional[str]=None) -> None:

    text.setText(textStr)
    if size:
        text.setSize(size)
    if foregroundColor:
        text.setTextColor(foregroundColor)

def DrawText(window:GraphWin, pointX:int, pointY:int, textStr:str, size:Optional[int]=None,
    lineColor:Optional[str]=None) -> Text:
    text = Text(Point(pointX, pointY), textStr)
    UpdateText(window, text, textStr, size, lineColor)
    text.draw(window)
    return text

def DrawPolygon(window:GraphWin, points:List,
    fillColor:str, lineColor:str='black', lineWidth:int=1) -> None:
    polygon = Polygon(points)
    polygon.setFill(fillColor)
    polygon.setOutline(lineColor)
    polygon.setWidth(lineWidth)  # width of boundary line
    polygon.draw(window)

def getMouseClick(window:GraphWin) -> Any:
    return window.getMouse()

def WaitForMouseClick(window:GraphWin) -> None:
    try:
        window.getMouse()
    except:
        pass

def CloseWindow(window:GraphWin) -> None:
    window.close()

def WaitForMouseClickAndCloseWindow(window:GraphWin):
    WaitForMouseClick(window)
    CloseWindow(window)
