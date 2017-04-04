'''
    Simulasi FIRA Robosot 
    Oleh Arif Rahman (arif@astanadigital.com)
    
    Example 2a - Bergerak ke arah objek berwarna
    
'''

import cv2
import numpy as np
import imutils
import arif

# Initialize VREP-ARIF simulation 
sim = arif.simulation().start()
# Get the camera and robot instances 
cap = arif.VideoCapture(sim,'v0')
robot = arif.PioneerP3DX(sim)


while(1):
    ret, img = cap.read()   # capture a frame from the camera 
    cv2.imshow("Image",img) # then display 
    
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(img, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only orange colors
    lower_hsv = np.array([5,70,70])
    upper_hsv = np.array([20,255,255])

    # Threshold the HSV image to get the colors
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    cv2.imshow("Mask",mask)

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


