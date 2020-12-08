from LibGraphics.graphics import *
from typing import Any, List, Optional

def CreateWindow(windowSizeX:int, windowSizeY:int, windowTitle:Optional[str]=None,
    backgroundColor:Optional[str]=None) -> GraphWin:
    if windowTitle == None:
        windowTitle = 'Window'
    window = GraphWin(windowTitle, windowSizeX, windowSizeY) # give title and dimensions
    if backgroundColor:
        window.setBackground(backgroundColor)
    window.setCoords(0, 0, windowSizeX, windowSizeY)
    return window

def DrawPoint(window:GraphWin, point:Any) -> None:
    point.draw(window)

def DrawCircle(window:GraphWin, circleCenterX:int, circleCenterY:int, radius:int, color:str) -> Circle:
    circle = Circle(Point(circleCenterX, circleCenterY), radius) # set center and radius
    circle.setFill(color)
    circle.draw(window)
    return circle

def DrawLine(window:GraphWin, point1X:int, point1Y:int, point2X:int, point2Y:int, width:int) -> Line:
    line = Line(Point(point1X, point1Y), Point(point2X, point2Y)) # set line points
    line.setWidth(width)
    line.draw(window)
    return line

def DrawOval(window:GraphWin, point1X:int, point1Y:int, point2X:int, point2Y:int, color:str) -> Oval:
    oval = Oval(Point(point1X, point1Y), Point(point2X, point2Y)) # set corners of bounding box
    oval.setFill(color)
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
    foregroundColor:Optional[str]=None) -> Text:
    text = Text(Point(pointX, pointY), textStr)
    UpdateText(window, text, textStr, size, foregroundColor)
    text.draw(window)
    return text

def DrawPolygon(window:GraphWin, points:List, lineWidth:int, backgroundColor:str,
    foregroundColor:str) -> None:
    polygon = Polygon(points)
    polygon.setFill(backgroundColor)
    polygon.setOutline(foregroundColor)
    polygon.setWidth(lineWidth)  # width of boundary line
    polygon.draw(window)

def getMouseClick(window:GraphWin) -> Any:
    return window.getMouse()

def WaitForMouseClick(window:GraphWin) -> None:
    window.getMouse()

def CloseWindow(window:GraphWin) -> None:
    window.close()

