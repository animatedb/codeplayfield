'''Draw rectangles using loops and functions.
'''

from LibGraphics.Graphics import *


def main():
    # Create a window that will show on the screen.
    # The size is 200 width and 150 height.
    window = CreateWindow(200, 150)

    # Draw 25 red points in X direction starting at X=20, and Y=10
    x = 20
    y = 10
    xAdd = 1
    yAdd = 0
    pointCounter = 0
    numberOfPoints = 25
    while(pointCounter < numberOfPoints):
        DrawPoint(window, x, y, 'red')
        x = x + xAdd
        y = y + yAdd
        pointCounter = pointCounter + 1

    # Draw 15 red points in Y direction starting at X=20, and Y=10
    x = 20
    y = 10
    xAdd = 0
    yAdd = 1
    pointCounter = 0
    numberOfPoints = 15
    while(pointCounter < numberOfPoints):
        DrawPoint(window, x, y, 'red')
        x = x + xAdd
        y = y + yAdd
        pointCounter = pointCounter + 1

    # Draw 25 red points in X direction starting at X=20, and Y=10+15
    x = 20
    y = 10+15
    xAdd = 1
    yAdd = 0
    pointCounter = 0
    numberOfPoints = 25
    while(pointCounter < numberOfPoints):
        DrawPoint(window, x, y, 'red')
        x = x + xAdd
        y = y + yAdd
        pointCounter = pointCounter + 1

    # Draw 15 red points in Y direction starting at X=20+15, and Y=10
    x = 20+25
    y = 10
    xAdd = 0
    yAdd = 1
    pointCounter = 0
    numberOfPoints = 15
    while(pointCounter < numberOfPoints):
        DrawPoint(window, x, y, 'red')
        x = x + xAdd
        y = y + yAdd
        pointCounter = pointCounter + 1

    # Draw a blue rectangle 30 below the top left of the previous rectangle
    drawLine(window, 20, 10+30, 1, 0, 25, 'blue')
    drawLine(window, 20, 10+30, 0, 1, 15, 'blue')
    drawLine(window, 20, 25+30, 1, 0, 25, 'blue')
    drawLine(window, 45, 10+30, 0, 1, 15, 'blue')

    # Draw a green rectangle 30 to the right of the top left of the previous rectangle
    drawRectangle(window, 20+30, 10, 25, 15, 'green')

    WaitForMouseClick(window)
    CloseWindow(window)


def drawLine(window, x, y, xAdd, yAdd, numberOfPoints, color):
    pointCounter = 0
    while(pointCounter < numberOfPoints):
        DrawPoint(window, x, y, color)
        x = x + xAdd
        y = y + yAdd
        pointCounter = pointCounter + 1

def drawRectangle(window, x, y, xSize, ySize, color):
    drawLine(window, x, y, 1, 0, xSize, color)
    drawLine(window, x, y, 0, 1, ySize, color)
    drawLine(window, x, y+ySize, 1, 0, xSize, color)
    drawLine(window, x+xSize, y, 0, 1, ySize, color)

main()

