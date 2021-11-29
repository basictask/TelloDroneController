# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 17:14:59 2021

@author: Daniel Kuknyo
This script will be the template to send a notification to a phone via the Telegram API

STEPS TO TAKE BEFORE:
1) Get a Telegram account (free) using your phone number
Web: https://web.telegram.org Also download the Telegram Android. 

2) Go into settings (web or app) and set a username
This is needed to obtain an id which your bot will use to send messages to.

3) Send a message to RawDataBot to get your id
Just search for RawDataBot and send any message (hi will do). Take a note of your id.

4) Create your bot (which you'll command with HTTP requests)
Now search for BotFather and send the message /start. Help is displayed. 
Send the message /newbot and follow the instructions. 
Take a note of your token to access the HTTP API

TELEGRAM E-CHANNEL ID FOR WEDS
Alina: 923197636
Dani: 2140059741
Sofien: 2132359615
Mariam: 2144912667
"""

import requests

def send_notifications(ids, text, photoname):
    token = "2127036493:AAFzTiQxgRNerbsNAD__4NqpWyumUttImL0"
    url = f"https://api.telegram.org/bot{token}" # Here comes the token from step 4
    
    for idx in ids: # Send the message to each of the IDs gotten through the params
        photo = {'photo': open(photoname, 'rb')} # Photo to attach to image    
        params = {"chat_id": idx, "text": text} # Here comes the token from step 3
        r = requests.get(url + "/sendPhoto", params=params, files=photo)
        print(r.status_code, r.reason, r.content)
        print()
        
#ids = ['923197636', '2140059741', '2132359615', '2144912667']
ids = ['2140059741', '2144912667'] # This will contain the Telegram IDs to send messages to 
text = 'Fire in the hole!' # What message should be sent
photoname = 'frames/frame3.png'

send_notifications(ids, text, photoname)
