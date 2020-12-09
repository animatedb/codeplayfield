import cv2
from typing import Any, Optional

# @todo - add comments

def ReadImage(imageFilename:str) -> Any:  # @todo - find real type name (Any)
    return cv2.imread(imageFilename)

def DrawImage(image, windowName:Optional[str]=None) -> None:
    if windowName == None:
        windowName = ''
    cv2.imshow(windowName, image)

def WaitForKey() -> None:
    cv2.waitKey(0)

def _onMouseClick(event,x,y,flags,param):
    global mousePosX, mousePosY
    if event == cv2.EVENT_LBUTTONDOWN:
        mousePosX = x
        mousePosY = y

# This will also quit if the close button on the window is clicked.
def WaitForMouseClick(windowName:Optional[str]=None) -> None:
    global mousePosX, mousePosY
    mousePosX = -1
    mousePosY = -1
    if windowName == None:
        windowName = ''
    cv2.setMouseCallback(windowName, _onMouseClick)
    while True:
        keyCode = cv2.waitKey(1)
#        if (keyCode & 0xFF) == 27:	# This will quit on the Esc key.
#    	    break
        if mousePosX != -1:
            break
        try:
            # This throws an exception if the window is closed.
            cv2.getWindowProperty(windowName, 0)
        except:    # Catch the exception if the window is closed.
            # Abort the loop
            break

def CloseWindows() -> None:
    cv2.destroyAllWindows()

