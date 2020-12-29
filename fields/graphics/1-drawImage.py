# To run this program
# Change directory to fields/graphics.
# Enter "python3 1-drawImage.py"
# Or "python 1-drawImage.py"

# Load a library that allows drawing and images.
from LibGraphics.Graphics import *

# Create a window that will show on the screen.
# The size is 300 width and 150 height.
window = CreateWindow(300, 150)

# The image was downloaded from the internet at "cleanpng.com".
# Draw the image on to the screen.
DrawImage(window, 0, 0, 'pict-pets.png')

# Wait for a mouse button click
WaitForMouseClick(window)

# Close window
CloseWindow(window)
