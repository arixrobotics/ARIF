'''
    Simulasi FIRA Robosot 
    Oleh Arif Rahman (arif@astanadigital.com)
    
    Example 4 - 'Align' diri dengan lantai
    
'''

import cv2
import numpy as np
import imutils
import math 

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

# Threshold the HSV image for only orange colors
hsv_range = {   'lower_green'   :   np.array([58,70,70]),
                'upper_green'   :   np.array([71,255,255]),
                'lower_blue'    :   np.array([115,70,70]),
                'upper_blue'    :   np.array([128,255,255]),
                'lower_yellow'  :   np.array([28,70,70]),
                'upper_yellow'  :   np.array([49,255,255]),
                'lower_red'     :   np.array([0,70,70]),
                'upper_red'     :   np.array([26,255,255])
            }
while(1):
    ret, img = cap.read()   # capture a frame from the camera 
    img = imutils.resize(img, width=300)
    h,w = img.shape[:2]
    img = img[h/2:h,0:w]
    h,w = img.shape[:2]
    # cv2.imshow("Image",img) # then display 
    
    # Blur the image to reduce noise
    blurred = cv2.GaussianBlur(img, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get the colors
    masked = {  'green'   : cv2.inRange(hsv, hsv_range['lower_green'], hsv_range['upper_green']),
                'blue'  : cv2.inRange(hsv, hsv_range['lower_blue'], hsv_range['upper_blue']),
                'yellow': cv2.inRange(hsv, hsv_range['lower_yellow'], hsv_range['upper_yellow']),
                'red'   : cv2.inRange(hsv, hsv_range['lower_red'], hsv_range['upper_red'])
            }
    # cv2.imshow("Mask Green",masked['green'])
    
    # Dilate each colour level 
    kernel = np.ones((5,5),np.uint8)
    for colour in masked:     # cannot iterate bcos dict is not iteratable 
        masked[colour] = cv2.dilate(masked[colour],kernel,iterations = 1)

        
    # Get the colour we are standing on now
    # by sidefilling from a spot right in front of the robot.
    # First get the edged image
    edged = cv2.Canny(blurred, 30, 150)
    # cv2.imshow("Edges", edged)
    # dilate to close any tiny gaps 
    dilated = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
    cv2.imshow("Dilated", dilated)
    
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    ffmask = np.zeros((h+2, w+2), np.uint8)
    
    # Floodfill from a point just in front of the robot
    fx = w/2
    fy = h - 10
    floodfill = dilated.copy()
    cv2.floodFill(floodfill, ffmask, (fx,fy), 255)
    # erode to remove obstacle outline
    floodfill = cv2.erode(floodfill,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)),iterations = 1)
    # Dilate a bit so that we can get an overlap 
    kernel = np.ones((5,5),np.uint8)
    floodfill = cv2.dilate(floodfill ,kernel,iterations = 1)
    cv2.imshow("Floodfilled", floodfill)
       
    # Next, find the overlap between the current floor and all the other colours. 
    i = 0
    line = np.zeros((img.shape[0],img.shape[1],1),np.uint8)
    for colour in masked:
        # diff = cv2.bitwise_and(floodfill,floodfill,mask = masked[colour])
        overlap = cv2.bitwise_and(floodfill,masked[colour])
        # cv2.imshow("Overlap: "+colour,overlap)
        # Calculate the percentage of overlap
        po = ((np.sum(overlap)/255.0)/(overlap.shape[0]*overlap.shape[1]))*100.0
        # print "Overlap: " + colour + " " + str(po)
        if 0.1 < po < 10: 
            line = overlap 
    cv2.imshow("Line",line)
    # approximate a straight line, then find the line's rotation angle 
    (_,cnts, _) = cv2.findContours(line.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:3]
    # cv2.drawContours(img, cnts, -1, (0,255,0), 3)
    line_angle = 0.0
    if len(cnts) > 0:
        cnt = cnts[0]
        rows,cols = img.shape[:2]
        [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        cv2.line(img,(cols-1,righty),(0,lefty),(0,255,124),2)
        line_angle = (math.tan(vy/vx)*180/math.pi)
    
    # move the robot based on the line angle 
    kp = 0.1
    steer = kp * line_angle
    if steer > 1: steer = 1
    if steer <-1: steer =-1
    robot.pioneer_drive(1, steer)
    
    cv2.imshow("Image",img)

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


