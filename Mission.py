# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:12:12 2021

This program will be a modular solution for Tello to do a mission

@author: Daniel Kuknyo
"""

from tello import Tello
import cv2

def do_mission(path):
    tello = Tello()
    tello.connect()
    tello.streamon()
    tello.takeoff()
    
    
    for i in range(4):
        frame = tello.get_frame_read().frame
        framepth = path+"frame"+str(i)+".png"
        cv2.imwrite(framepth, frame)
        tello.rotate_clockwise(90)
    
    tello.land()
