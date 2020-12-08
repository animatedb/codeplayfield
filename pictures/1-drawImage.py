# To run this program
# Change directory to teach/drawing.
# Enter "python3 1-drawImage.py"

# Load a library that allows drawing and images.
from LibImage.Images import *

# The image was downloaded from the internet at "cleanpng.com".
image = ReadImage('1-pets.jpg')

# Draw the image on the screen.
DrawImage(image)

# Wait for a mouse button click
WaitForMouseClick()

# Close any windows
CloseWindows()

