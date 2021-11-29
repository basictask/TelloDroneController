# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:12:12 2021

This program will be a modular solution for Tello to do a mission

@author: Daniel Kuknyo
"""

from djitellopy import Tello
import cv2

def do_mission(path, init_imname, height):
    tello = Tello()
    tello.connect()
    tello.streamon()
    tello.takeoff()
    
    tello.move_up(height)
    
    for i in range(4):
        frame = tello.get_frame_read().frame
        framepth = path + init_imname + str(i) + ".png"
        cv2.imwrite(framepth, frame)
        print()
        print("Saving image: ", framepth)
        tello.rotate_clockwise(90)
    
    tello.move_down(height)
    
    tello.land()


if __name__ == 'main':
    rootdir = 'C:/Users/Daniel Kuknyo/Documents/GitHub/TelloDroneController/'
    directory = 'Images/'
    init_imname = 'frame'
    imgdir = rootdir + directory
    do_mission(imgdir, init_imname, 30)
