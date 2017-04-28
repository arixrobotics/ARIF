'''
    Simulasi FIRA Robosot 
    Oleh Arif Rahman (arif@astanadigital.com)
    
    Example 1 - Mengawal pergerakan robot Pioneer P3DX
    
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
robot = arif.PioneerP3DX(sim)


while(1):
    ret, img = cap.read()   # capture a frame from the camera 
    cv2.imshow("Image",img) # then display 
    
    # Check if any key is pressed 
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("w"):  # go forward
        robot.pioneer_drive(5, 0)     # speed, steer
        print "go forward"
    elif key == ord('s'):  # stop 
        robot.pioneer_drive(0, 0)
        print "stop"
    elif key == ord('x'):  # go reverse 
        robot.pioneer_drive(-5, 0)
        print "go reverse"
    elif key == ord("a"):  # rotate left
        robot.pioneer_drive(0, -3)
        print "rotate left"
    elif key == ord("q"):  # turn left
        robot.pioneer_drive(5, -1)
        print "turn left"
    elif key == ord('d'):  # rotate right
        robot.pioneer_drive(0, 3)
        print "rotate right"
    elif key == ord('e'):  # turn right
        robot.pioneer_drive(5, 1)
        print "turn right"
    if key == 27:   # esc
        break

# clean up before exiting 
cv2.destroyAllWindows()
arif.simulation().end()


