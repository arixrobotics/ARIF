''' 
    Using V-REP simulation with Python and OpenCV
    Muhammad Arif B Abdul Rahman
    March 2017
    
    inspired and modified from http://robologs.net/2016/07/07/tutorial-de-vrep-y-opencv-python/ 

'''

import vrep 
import math 
import time
import numpy as np
import cv2 
import sys 

class simulation:
    def __init__(self):
        pass
    
    def start(self):
        vrep.simxFinish(-1) # terminate any previous connection
        self.clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # connect to VREP server
        
        if self.clientID != -1:
            print ('Connected to VREP simulation server.')
            return self.clientID 
        else:
            sys.exit("Error: No connection! Please ensure VREP simulation has been started.")
        
    
    def end(self):
        vrep.simxFinish(-1)
        
class VideoCapture:
    ''' Retrieve images from a camera within VREP ''' 
    def __init__(self, id, cam):
        self.clientID = id
        # retrieve camera handle
        _, self.camhandle = vrep.simxGetObjectHandle(self.clientID, cam, vrep.simx_opmode_oneshot_wait)

        # Initialize camera 
        _, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_streaming)
        time.sleep(1)
        
    def read(self):
        # Grab frame from camera, rotate and convert to BGR 
        ret, resolution, image = vrep.simxGetVisionSensorImage(self.clientID, self.camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype = np.uint8)
        img.resize([resolution[1], resolution[0], 3])
        img = np.rot90(img,2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return ret,img 
        
class PioneerP3DX:
    ''' Pioneer P3DX differential drive robot '''
    def __init__(self, clientID, m1='',m2=''):
        self.clientID = clientID
        if m1 == '':
            m1 = 'Pioneer_p3dx_leftMotor'
            m2 = 'Pioneer_p3dx_rightMotor'
        # retrieve motor handles
        errorCode, self.left_motor_handle  = vrep.simxGetObjectHandle(self.clientID, m1, vrep.simx_opmode_oneshot_wait)
        errorCode, self.right_motor_handle = vrep.simxGetObjectHandle(self.clientID, m2, vrep.simx_opmode_oneshot_wait)
        if not errorCode == vrep.simx_return_ok:
            sys.exit("Error: Could not connect to robot! Please ensure correct robot configuration has been made.")
         
    def pioneer_drive(self, speed, steer=0, k_steer=0.5):
        vl = speed + k_steer*steer
        vr = speed - k_steer*steer
        vrep.simxSetJointTargetVelocity(self.clientID, self.left_motor_handle,  vl, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(self.clientID, self.right_motor_handle, vr, vrep.simx_opmode_streaming)
            
class OmniPlatform:
    ''' An omni-directional robot using mecannum wheels '''
    def __init__(self, clientID, m1='',m2='',m3='',m4=''):
        self.clientID = clientID
        if m1 == '':
            m1 = 'OmniWheel_regularRotation'
            m2 = 'OmniWheel_regularRotation#0'
            m3 = 'OmniWheel_regularRotation#1'
            m4 = 'OmniWheel_regularRotation#2'
        # retrieve motor handles
        errorCode, self.omni_wheel_handle_0 = vrep.simxGetObjectHandle(self.clientID, m1, vrep.simx_opmode_oneshot_wait)
        errorCode, self.omni_wheel_handle_1 = vrep.simxGetObjectHandle(self.clientID, m2, vrep.simx_opmode_oneshot_wait)
        errorCode, self.omni_wheel_handle_2 = vrep.simxGetObjectHandle(self.clientID, m3, vrep.simx_opmode_oneshot_wait)
        errorCode, self.omni_wheel_handle_3 = vrep.simxGetObjectHandle(self.clientID, m4, vrep.simx_opmode_oneshot_wait)
        if not errorCode == vrep.simx_return_ok:
            sys.exit("Error: Could not connect to robot! Please ensure correct robot configuration has been made.")
            
    def omni_move(self, speed, direction="stop"):
        speed = speed*2.398795*math.pi/180 # 2.398795 is a factor needed to obtain the right pad rotation speed
        if direction == "forward":
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_0,-speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_1,-speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_2,speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_3,speed, vrep.simx_opmode_streaming)
        elif direction == "right":
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_0,-speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_1,speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_2,speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_3,-speed, vrep.simx_opmode_streaming)
        elif direction == "left":
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_0,speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_1,-speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_2,-speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_3,speed, vrep.simx_opmode_streaming)
        elif direction == "reverse":
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_0,speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_1,speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_2,-speed, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_3,-speed, vrep.simx_opmode_streaming)
        elif direction == "stop":
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_0,0, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_1,0, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_2,0, vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(self.clientID,self.omni_wheel_handle_3,0, vrep.simx_opmode_streaming)