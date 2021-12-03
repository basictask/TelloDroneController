# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 10:21:23 2021

@author: Daniel Kuknyo

This program will use pygame to control the drone

Maintains the Tello display and moves it through the keyboard keys.
Press escape key to quit.
The controls are:
    - T: Takeoff
    - L: Land
    - Arrow keys: Forward, backward, left and right.
    - A and D: Counter clockwise and clockwise rotations (yaw)
    - W and S: Up and down.
    - P: take photo and save it to given image folder --> Program needs to recieve this as parameter!

The purpose of a mission is to save images into a given folder with a given name so the main 
program of the Tello drone controller can read it.
The image name and directory will have to be recieved through the parameters. 
Image file format is png.

For available Tello commands refer to tello.py --> methods inside class file
"""

from djitellopy import Tello
from datetime import date
import cv2
import pygame
import numpy as np
import time

# Speed of the drone
S = 30
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
# pygame
FPS = 30

class FrontEnd(object):
    def __init__(self, path, init_imname):
        pygame.init() # Init pygame

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10
        self.send_rc_control = False
        self.image_counter = 0
        self.path = path
        self.init_imname = init_imname

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def run(self):
        self.tello.connect()
        self.tello.set_speed(self.speed)

        self.tello.streamoff() # In case streaming is on.
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S
        elif key == pygame.K_p: # take a photo and save it into a given folder
            frame_img = self.tello.get_frame_read().frame
            frame_name = self.path + self.init_imname + str(self.image_counter) + ".png"
            cv2.imwrite(frame_name, frame_img)
            self.image_counter += 1

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key -> Button pressed
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)

def manual_misson(path, init_imname):
    frontend = FrontEnd(path, init_imname)
    frontend.run()

if __name__ == '__main__':
    # Set up variables
    rootdir = 'C:/Users/Daniel Kuknyo/Documents/GitHub/TelloDroneController/Images/' # Where the image folder is
    directory = 'frames/' # Image folder name
    today = str(date.today())
    init_imname = today + '_frame' # Image name fixed part: e.g. frame0.png, frame1.png etc...
    imgdir = rootdir + directory
    
    # Run mission
    manual_misson(path=imgdir, init_imname=init_imname)
