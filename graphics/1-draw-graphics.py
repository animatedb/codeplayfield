# From http://anh.cs.luc.edu/handsonPythonTutorial/graphics.html
'''A simple graphics example constructs a face from basic shapes.
'''

from LibGraphics.Graphics import *


def main():
    window = CreateWindow(200, 150)

    # Head
    DrawCircle(window, 40, 100, 25, 'yellow')

    # Eye
    DrawCircle(window, 30, 105, 5, 'blue')

    # Other eye
    DrawLine(window, 45, 105, 55, 105, 3)

    # Mouth
    DrawOval(window, 30, 90, 50, 85, 'red')

    DrawText(window, 100, 120, 'A face')

    DrawText(window, window.getWidth()/2, 20, 'Click anywhere to quit.')

    WaitForMouseClick(window)
    CloseWindow(window)

main()

