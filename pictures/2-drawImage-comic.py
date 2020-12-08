# To run this program
# Change directory to teach/drawing.
# Enter "python3 1-drawImage.py"

# Load a library that allows drawing and images.
from LibImage.Images import *

# The image was drawn in gimp.
image = ReadImage('2-fish-1.png')

# Draw the image on the screen.
DrawImage(image)

# Wait for a mouse button click
WaitForMouseClick()

image = ReadImage('2-fish-2.png')
DrawImage(image)

# Wait for a mouse button click
WaitForMouseClick()

# Close any windows
CloseWindows()

