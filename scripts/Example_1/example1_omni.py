'''
    Simulasi FIRA Robosot 
    Oleh Arif Rahman (arif@astanadigital.com)
    
    Example 1 - Mengawal pergerakan robot OmniPlatform
    
'''

import cv2
import numpy as np
import imutils

'''--- For using the ARIF simulation ---'''
import sys, os 
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
os.chdir("..\\ariflib") # <-- if in Windows
# os.chdir("../ariflib") # <-- if in Linux
from ariflib import arif
'''--------------------------------------'''

# Initialize VREP-ARIF simulation 
sim = arif.simulation().start()
# Get the camera and robot instances 
cap = arif.VideoCapture(sim,'v0')
robot = arif.OmniPlatform(sim)


while(1):
    ret, img = cap.read()   # capture a frame from the camera 
    cv2.imshow("Image",img) # then display 
    
    # Check if any key is pressed 
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("w"):  # go forward
        robot.omni_move(100, "forward")
        print "go forward"
    elif key == ord("a"):  # go left
        robot.omni_move(100, "left")
        print "go left"
    elif key == ord('x'):  # go reverse 
        robot.omni_move(100, "reverse")
        print "go reverse"
    elif key == ord('d'):  # go right
        robot.omni_move(100, "right")
        print "go right"
    elif key == ord('s'):  # stop 
        robot.omni_move(0)
        print "stop"
    if key == 27:   # esc
        break

# clean up before exiting 
cv2.destroyAllWindows()
arif.simulation().end()


