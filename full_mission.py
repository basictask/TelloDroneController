# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 14:21:53 2021

@author: Daniel Kuknyo

This is the program that handles the mission for the Tello drone.

### Program description ###
The program will read and load resnet into a torchvision model file, already pretrained on fire/nonfire pictures.
The program will connect to the drone using an UDP connection and a specific port reserved for this.
The drone will take off, take 4 pictures in each direction (forward, backward, left, right). 
The leaded torchvision model evalates the pictures, depending if it's fire or not.
If there's a fire showing up on any of the photos, the drone will send notification to a specified group of people.
Notification sending works by commanding a previously defined telegram bot controlled by HTTP requests. 
For connection with wifi settings refer to wifitest.py

Changelog:
Added customizable mission to program e.g. mission library 
New mission added: drone can be controlled with pygame
"""

#%% Libraries used
import requests
import cv2
import os
import winwifi
import torch
import torchvision
from torchvision import transforms
from Mission import do_mission

rootdir = 'C:/Users/Daniel Kuknyo/Documents/GitHub/TelloDroneController/'
directory = 'Images/'
init_imname = 'frame'
imgdir = rootdir + directory
os.chdir(rootdir) # Can be any directory, but needs an Images subfolder


#%% Read model file into torchvision
model = torch.load('ResNet18', map_location=torch.device('cpu'))

im_height = 224
im_width = 224
img_transforms = transforms.Compose([transforms.ToTensor(), 
                                     torchvision.transforms.Resize((im_height, im_width))])


#%% This function will send notifications to a specified group
group = {'Alina': '923197636', 'Dani': '2140059741', 'Mariam': '2144912667', 'Sofien': '2132359615'}
names = ['Dani', 'Mariam', 'Sofien'] # This will contain the Telegram IDs to send messages to 
text = 'Fire in the hole!' # What message should be sent

def send_notifications(names, text, photoname):
    token = "2127036493:AAFzTiQxgRNerbsNAD__4NqpWyumUttImL0"
    url = f"https://api.telegram.org/bot{token}" # Here comes the token from step 4
    ids = [group[x] for x in names]
    
    for idx in ids: # Send the message to each of the IDs gotten through the params
        photo = {'photo': open(photoname, 'rb')} # Photo to attach to image    
        params = {"chat_id": idx, "text": text} # Here comes the token from step 3
        r = requests.get(url + "/sendPhoto", params=params, files=photo)
        print(r.status_code, r.reason, r.content)
        print()
        

#%% Fly the drone and save the images
# Params: directory, image fixed part (for saving), height (to fly up and down)
# Images will be saved into imgdir Images folder. Torch imagefolder will read them from here
do_mission(imgdir, init_imname, 30) 


#%% Iterate over the images using torchvision model 
preds = {}
images = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        img = cv2.imread(f)
        images.append(img)
        img_trans = img_transforms(img)
        output = model(img_trans)
        preds[f] = output
        
        
#%% Iterate over predictions to check if there's a fire
winwifi.WinWiFi.connect('Kknet') # Connect to Wifi with gateway to internet

for key in preds.keys():
    photoname = directory + key
    if (model[key] == 1): # There's a fire
        text = 'Fire detected!'
        send_notifications(names, text, photoname)
    else: # No fire detected on given image
        text = 'No fire on this image'
        send_notifications(names, text, photoname)
        
