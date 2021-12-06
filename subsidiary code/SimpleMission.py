# -*- coding: utf-8 -*-
# This program will make the drone take off, and take a picture in every direcetion
from djitellopy import Tello
import cv2, math, time

 
#%% Estabilish connection
tello = Tello()
tello.connect()


#%% Turn on video
tello.streamon()


#%% Do some basic commands
tello.takeoff()

time.sleep(6) # wait 
image = tello.get_frame_read().frame
tello.rotate_counter_clockwise(90) # For some reason this doesn't work
cv2.imwrite('frame.jpg', image)
tello.land()


#%% 
cv2.imwrite('frame.jpg', image)
cv2.imshow('drone', image)
cv2.waitKey(0)
