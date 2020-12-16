import os
import sys
import subprocess
os.chdir('../fields/graphics')

subprocess.check_call([sys.executable, "-m", "pip", "install", 'opencv-python'])

from LibGraphics.Graphics import *

os.chdir('../../jupyter')
