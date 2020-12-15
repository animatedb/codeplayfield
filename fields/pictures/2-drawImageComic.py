# To run this program
# Change directory to teach/drawing.
# Enter "python3 1-drawImage.py"

# Load a library that allows drawing and images.
from LibImage.Images import *

# Read an image file from disk into memory.
# The image was drawn in gimp.
image = ReadImage('2-fish-1.png')

# Draw the image from memory on to the screen.
DrawImage(image)

# Wait for a mouse button click
WaitForMouseClick()

# Read another image file from disk into memory.
image = ReadImage('2-fish-2.png')
# Draw the image from memory on to the screen.
DrawImage(image)

# Wait for a mouse button click
WaitForMouseClick()

# Close any windows
CloseWindows()

