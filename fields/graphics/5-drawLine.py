# From http://anh.cs.luc.edu/handsonPythonTutorial/graphics.html
'''A simple graphics example constructs a face from basic shapes.
'''

from LibGraphics.Graphics import *


def main():
    # Create a window that will show on the screen.
    # The size is 200 width and 150 height.
    window = CreateWindow(200, 150)

    # Draw a blue point at X=20, Y=10
    DrawPoint(window, 20, 10, 'blue')

    # Draw many red points starting at X=30, and Y=20
    keepGoing = True
    x = 30
    while(keepGoing):
        DrawPoint(window, x, 20, 'red')
        x = x + 1
        if x == 50:
            keepGoing = False

    # Draw many green points starting at X=30, and Y=35
    keepGoing = True
    x = 30
    y = 35
    while(keepGoing):
        DrawPoint(window, x, y, 'green')
        y = y + 1
        if y == 50:
            keepGoing = False

    # Draw many purple points starting at X=40, and Y=35
    keepGoing = True
    x = 40
    y = 35
    xAdd = 1
    yAdd = 0.25
    while(keepGoing):
        DrawPoint(window, x, y, 'purple')
        x = x + xAdd
        y = y + yAdd
        if y == 60:
            keepGoing = False

    WaitForMouseClick(window)
    CloseWindow(window)

main()

