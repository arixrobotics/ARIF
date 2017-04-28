'''
    Simulasi FIRA Robosot 
    Oleh Arif Rahman (arif@astanadigital.com)
    
    Example 3 - Mengelak halangan 
    Scene: OmniPlatform_multi_obstacle.ttt
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

raw_input("Press enter to begin.")

while(1):
    ret, img = cap.read()   # capture a frame from the camera 
    img = imutils.resize(img, width=300)
    h,w = img.shape[:2]
    cv2.imshow("1. Original", img)
    
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("2. Gray", gray)

    # blur a bit to remove noise 
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    cv2.imshow("3. Blurred", blurred)

    # find any edges 
    edged = cv2.Canny(blurred, 30, 150)
    cv2.imshow("4. Edges", edged)
    
    # dilate to close any tiny gaps 
    dilated = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
    cv2.imshow("5. Dilated", dilated)
    
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Floodfill from a point just in front of the robot
    fx = w/2
    fy = h - 30
    floodfill = dilated.copy()
    cv2.floodFill(floodfill, mask, (fx,fy), 255)
    # erode to remove obstacle outline
    floodfill = cv2.erode(floodfill,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)),iterations = 1)
    cv2.imshow("6. Floodfilled",floodfill)
    
    # next find the obstacle's distance to robot 
    obstacle = cv2.bitwise_not(floodfill)
    cv2.imshow("7. Obstacles",obstacle)
    
    # if obstacle present, calculate extreme points
    if obstacle.any():
        # first find the contours
        _, cnts, _ = cv2.findContours(obstacle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print "cnts:{}".format(len(cnts))
        # then find the bottommost point of each contour. 
        # this point is the point nearest to the robot 
        obstacle_lowest = (0,0)
        for c in cnts:
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])
            if extBot[1] > obstacle_lowest[1]:
                obstacle_lowest = extBot
        print obstacle_lowest
        
        # if this obstacle point is far from robot, go forward 
        if obstacle_lowest[1] < (h*0.8):
            robot.omni_move(100,"forward")
            print "go forward"
        # else, go left or right
        # depending on whether the bottommost point is on the 
        # left or right of the robot 
        else: 
            if obstacle_lowest[0] < w/2:
                robot.omni_move(100,"right")
                print "go right"
            else:
                robot.omni_move(100,"left")
                print "go left"
    
    
    # draw some indications on the final image 
    # floodfill start point 
    cv2.circle(img,(fx,fy), 2, (100,0,100), -1)
    # bottommost obstacle point 
    cv2.circle(img,obstacle_lowest, 6, (100,0,255), -1)
    # obstacle lowest limit
    cv2.line(img, (0,int(h*0.8)), (w,int(h*0.8)), (100,100,0), 1)
    # then show 
    cv2.imshow("8. Final",img)
    
    
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
        robot.omni_move(100, "stop")
        print "stop"
    if key == 27:   # esc
        break

# clean up before exiting 
cv2.destroyAllWindows()
arif.simulation().end()


