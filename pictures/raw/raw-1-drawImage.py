
# Load a library that allows drawing and images.
import cv2 

# Save image in set directory 
# Read RGB image
# download image from cleanpng.com
img = cv2.imread('1-pets.jpg')  

# Output img with window name as 'image'
cv2.imshow('image', img)  

# Maintain output window util user presses a key 
cv2.waitKey(0)         

# Destroying present windows on screen 
cv2.destroyAllWindows()  

