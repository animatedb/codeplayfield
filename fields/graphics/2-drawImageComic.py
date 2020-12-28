# To run this program
# Change directory to teach/drawing.
# Enter "python3 1-drawImage.py"

# Load a library that allows drawing and images.
from LibGraphics.Graphics import *

# Create a window that will show on the screen.
# The size is 800 width and 600 height.
window = CreateWindow(800, 600)

# Draw the image on to the screen.
# The image was drawn in gimp.
DrawImage(window, 0, 0, 'comic-fish-1.png')

# Wait for a mouse button click
WaitForMouseClick(window)

# Draw another on to the screen.
DrawImage(window, 0, 0, 'comic-fish-2.png')

# Wait for a mouse button click
WaitForMouseClick(window)

# Close any windows
CloseWindows(window)

