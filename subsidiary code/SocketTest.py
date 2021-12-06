# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 15:56:00 2021

@author: Daniel Kuknyo
"""

from tello import Tello
from datetime import datetime
import time

start_time = str(datetime.now())

file_name = "commands.txt"

f = open(file_name, "r")
commands = f.readlines()

tello = Tello()
for command in commands:
    if command != '' and command != '\n':
        command = command.rstrip()

        if command.find('delay') != -1:
            sec = float(command.partition('delay')[2])
            print (sec)
            time.sleep(sec)
            pass
        else:
            tello.send_command(command)

log = tello.get_log()

out = open('log/' + start_time + '.txt', 'w')
for stat in log:
    stat.print_stats()
    str = stat.return_stats()
    out.write(str)
