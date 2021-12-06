# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 21:10:31 2021

@author: Daniel Kuknyo
"""

from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.rotate_clockwise(90)
tello.move_forward(10)

tello.land()
