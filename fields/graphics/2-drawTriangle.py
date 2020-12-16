# From http://anh.cs.luc.edu/handsonPythonTutorial/graphics.html
'''Program: triangle.py or triangle.pyw (best name for Windows)
Interactive graphics program to draw a triangle,
with prompts in a Text object and feedback via mouse clicks.
'''

from LibGraphics.Graphics import *

def main():
    window = CreateWindow(350, 350, 'Triangle', 'Yellow')

    text = DrawText(window, window.getWidth()/2, 320, 'Click at three places',
        lineColor='red')

    # Get and draw three vertices of triangle
    p1 = getMouseClick(window)
    DrawPoint(window, p1)
    p2 = getMouseClick(window)
    DrawPoint(window, p2)
    p3 = getMouseClick(window)
    DrawPoint(window, p3)
    points = [p1, p2, p3]

    # Use Polygon object to draw the triangle
    # Draw the points connected by a line with width of 4.
    DrawPolygon(window, points, 'gray', 'cyan', 4)

    UpdateText(window, text, 'Click anywhere to quit')
    WaitForMouseClick(window)
    CloseWindow(window) 

main()

