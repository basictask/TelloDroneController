# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 14:21:53 2021

@author: Daniel Kuknyo

### This is the program that handles the mission and interactions for the Tello drone. ###

### Program description ###
The program will read and load resnet into a torchvision model file, already pretrained on fire/nonfire pictures.
The program will connect to the drone using an UDP connection and a specific port reserved for this.
The drone will take off, take 4 pictures in each direction (forward, backward, left, right). 
The leaded torchvision model evalates the pictures, depending if it's fire or not.
If there's a fire showing up on any of the photos, the drone will send notification to a specified group of people.
Notification sending works by commanding a previously defined telegram bot controlled by HTTP requests. 
Important: the Telegram bot needs to be activated for the user. --> Verify by sending a message to Wedsbot
For connection with wifi settings refer to wifitest.py

Changelog:
Added customizable mission to program e.g. mission library 
Added switching between automatic and manual control modes
New mission added: drone can be controlled with pygame
"""

#%% Libraries used
print('Setting up dependecnies...')
import requests
import cv2
import os
import winwifi
import torch
import torchvision
from torchvision import transforms
from Mission import do_mission
from ManualControl import FrontEnd

# Directories and global variables needed to run mission # Configure them before running
mission_mode = 'auto' # auto -> predefined path; manual -> manually controlling the drone from python interface
model_name = 'ResNet18' # Which model to read from files
rootdir = 'C:/Users/Daniel Kuknyo/Documents/GitHub/TelloDroneController/Images/' # Where the image folder is
directory = 'frames/' # Image folder name
init_imname = 'frame' # Image name fixed part: e.g. frame0.png, frame1.png etc...
imgdir = rootdir + directory # Images directory absolute path
os.chdir(rootdir) # Can be any directory, but needs an Images subfolder


#%% Read model file into torchvision
print('Reading model file...')

model = torch.load(model_name, map_location=torch.device('cpu'))

# Transformations needed for the model file 
im_height = 224
im_width = 224
img_transforms = transforms.Compose([transforms.ToTensor(), 
                                     torchvision.transforms.Resize((im_height, im_width))])


#%% This function will send notifications to a specified group
# Below is every team member's name with the Telegram E-channel ID-s specified
print('Getting Telegram definitions...')

# A dict containing the team member name - ID associations
group = {'Alina': '923197636', 'Dani': '2140059741', 'Mariam': '2144912667', 'Sofien': '2132359615'} 
names = ['Dani', 'Mariam'] # This will contain the Telegram IDs to send messages to 
text = 'Fire in the hole!' # What message should be sent

def send_notifications(names, text, photoname):
    token = "2127036493:AAFzTiQxgRNerbsNAD__4NqpWyumUttImL0" # Telegram API token -> Dani
    url = f"https://api.telegram.org/bot{token}" # Here comes the token from step 4
    ids = [group[x] for x in names]
    
    for idx in ids: # Send the message to each of the IDs gotten through the params
        print(photoname)    
        photo = {'photo': open(photoname, 'rb')} # Photo to attach to image    
        params = {"chat_id": idx, "text": text} # Here comes the token from step 3
        rp = requests.get(url + "/sendPhoto", params=params, files=photo)
        rm = requests.get(url + "/sendMessage", params=params)
        print(rp.status_code, rp.reason, rp.content) # Send image 
        print(rm.status_code, rm.reason, rm.content) # Send text message (Fire/no fire)
        print()
        

#%% Fly the drone and save the images
# Images will be saved into imgdir Images folder. Torch imagefolder will read them from here
# The purpose of the mission is to save the drone images into the folder recieved through the params
print('Drone mission starting...')

if(mission_mode == 'auto'):
    ##### Predefined mission course #####
    # Params: directory, image fixed part (for saving), height (to fly up and down), angle (in degrees) to turn, number of times to turn
    do_mission(imgdir, init_imname, 30, 90, 4) 
    
elif(mission_mode == 'manual'):
    ##### Other possibility #####
    # Uncomment part below to make it work
    # This class will allow Tello to be controlled by a preson with the keyboard
    ## Controls ##
    # - T: Takeoff
    # - L: Land
    # - Arrow keys: Forward, backward, left and right.
    # - A and D: Counter clockwise and clockwise rotations (yaw)
    # - W and S: Up and down.
    # - P: take photo and save it to given image folder
    frontend = FrontEnd()
    frontend.run()
    
print('Mission successful!')

#%% Iterate over the images using torchvision model 
# Read all the data saved by the mission into a datafolder
print('Reading the images saved by the drone...')

train_data = torchvision.datasets.ImageFolder(root=rootdir, transform=img_transforms)
train_data_loader = torch.utils.data.DataLoader(train_data, batch_size=1)

print('Creating predictions...')
preds = []
images = []
for batch in train_data_loader: # Iterate over the loader and create a prediction for every image
    inputs, targets = batch # Unpacking
    outputs = model(inputs) # Create prediction
    images.append(inputs)
    pred = float(outputs[0][0]) > 0 # Decide if it's a fire image or not
    preds.append(pred)


#%% This step is needed to be able to send the notifications -> notif. problem occurs 
# If not with this Wifi name, input any wifi network SSID that is saved by the laptop that's running the python interface
print('Estabilishing connection to gateway...')
winwifi.WinWiFi.connect('Kknet') # Connect to Wifi with gateway to internet        
        

#%% Iterate over predictions to check if there's a fire
print('Successfully connected to gateway. Sending out notifications.')

i = 0
for filename in os.listdir(imgdir): # Iterate over the image directory
    pred = preds[i]
    photoname = os.path.join(directory, filename)
    if os.path.isfile(photoname):
        if (pred): # There's a fire
            text = 'Fire detected!'
            send_notifications(names, text, photoname)
        else: # No fire detected on given image
            text = 'No fire on this image'
            send_notifications(names, text, photoname)
    i += 1

print('City saved. Exiting.')
