'''
    Simulasi FIRA Robosot 
    Oleh Arif Rahman (arif@astanadigital.com)
    
    Example 2a - Bergerak ke arah objek berwarna
    
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
    
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(img, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only orange colors
    lower_hsv = np.array([5,70,70])
    upper_hsv = np.array([20,255,255])

    # Threshold the HSV image to get the colors
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Take the moments to get the area and centroid
    moments = cv2.moments(mask)
    area = moments['m00']
    centroid_x, centroid_y = None, None
    if area != 0:
        centroid_x = int(moments['m10']/area)
        centroid_y = int(moments['m01']/area)
        ctr = (centroid_x, centroid_y)
    else:
        ctr = None
        
    print "(x,y):{} area:{}".format(ctr,area)
        
    # Draw some markers on the image so that we can visualize
    # centroid
    if not ctr == None:
        cv2.circle(img,ctr, 5, (0,0,250), 2)    

    # Then display images
    cv2.imshow("Image",img)
    cv2.imshow("Mask",mask)
    
    # Check if esc key is pressed 
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


