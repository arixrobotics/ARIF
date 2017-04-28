#!/usr/bin/env python
# -*- coding: utf-8 -*-

# USAGE: 
# Do this if you want to use the webcam:
# $ python colour_range_finder.py --webcam 
#
# Or this is you want to use the VREP simulation:
# $ python colour_range_finder.py
#

import cv2
import argparse
from operator import xor
'''--- For using the ARIF simulation ---'''
import sys, os 
sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
os.chdir("..\\ariflib") # <-- if in Windows
# os.chdir("../ariflib") # <-- if in Linux
from ariflib import arif
'''--------------------------------------'''

def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for j in range_filter:
        for i in ["MIN", "MAX"]:
            vmax = 255
            if i == "MIN":
                v = 0 
            elif j == "H": 
                v = 179
                vmax = 179
            else: 
                v = 255 
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, vmax, callback)


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=False,
                    help='Range filter. RGB or HSV')
    ap.add_argument('-i', '--image', required=False,
                    help='Path to the image')
    ap.add_argument('-w', '--webcam', required=False,
                    help='Use webcam', action='store_true')
    ap.add_argument('-p', '--preview', required=False,
                    help='Show a preview of the image after applying the mask',
                    action='store_true')
    args = vars(ap.parse_args())

    # if not xor(bool(args['image']), bool(args['webcam'])):
        # ap.error("Please specify only one image source")

    # if not args['filter'].upper() in ['RGB', 'HSV']:
        # ap.error("Please speciy a correct filter.")
    if not args['filter']:
        args['filter'] = 'HSV'

    return args


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values


def main():
    args = get_arguments()

    range_filter = args['filter'].upper()

    # if args['image']:
        # image = cv2.imread(args['image'])

        # if range_filter == 'RGB':
            # frame_to_thresh = image.copy()
        # else:
            # frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # else:
        # camera = cv2.VideoCapture(0)	# change 0 to 1 to change webcam number

    if args['webcam']:
        camera = cv2.VideoCapture(0)	# change 0 to 1 to change webcam number
    else:
        # Initialize VREP-ARIF simulation 
        sim = arif.simulation().start()
        # Get the camera instance 
        camera = arif.VideoCapture(sim,'v0')
        
    setup_trackbars(range_filter)

    while True:
        # if args['webcam']:
        ret, image = camera.read()

        # if not ret:
            # break

        if range_filter == 'RGB':
            frame_to_thresh = image.copy()
        else:
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        if args['preview']:
            preview = cv2.bitwise_and(image, image, mask=thresh)
            cv2.imshow("Preview", preview)
        else:
            cv2.imshow("Original", image)
            cv2.imshow("Thresh", thresh)

        if cv2.waitKey(1) & 0xFF is 27:
            break


if __name__ == '__main__':
    main()