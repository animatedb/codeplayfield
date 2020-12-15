# From http://anh.cs.luc.edu/handsonPythonTutorial/graphics.html
'''A simple graphics example constructs a face from basic shapes.
'''

from LibGraphics.Graphics import *


def main():
    # Create a window that will show on the screen.
    # The size is 200 width and 150 height.
    window = CreateWindow(200, 150)

    # Head
    # Draw a circle at X=40, Y=100, radius=25
    DrawCircle(window, 40, 100, 25, 'yellow')

    # Eye
    DrawCircle(window, 30, 105, 5, 'blue')

    # Other eye
    # Draw a line at point 1 X=45, y=105 to
    # point 2, x=55, y=105.
    # Width of the line is 3.
    DrawLine(window, 45, 105, 55, 105, 3)

    # Mouth
    # Draw an oval with point1=30,90 and point2 = 50,85
    DrawOval(window, 30, 90, 50, 85, 'red')

    # Draw some text at X=100, Y=120
    DrawText(window, 100, 120, 'A face')

    DrawText(window, window.getWidth()/2, 20, 'Click anywhere to quit.')

    WaitForMouseClick(window)
    CloseWindow(window)

main()

