import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import ctypes
from io import BytesIO
import requests
import six
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
import time
import subprocess


#from screeninfo import get_monitors

# C:\Users\nophi\PycharmProjects\spoo
class Wallify(object):


    def __init__(self,monitorW, monitorH):
        self.username = '0'
        self.client_id = 'd50af8bb2fe2476fba04e2a743334948'
        self.client_secret = '122ed6bfe1984330b802933f1f42854b'
        self.scope = 'user-read-private user-read-playback-state'
        self.redirectUri = 'https://www.google.com'
        self.token = util.prompt_for_user_token(self.username,scope=self.scope,client_id=self.client_id,client_secret=self.client_secret, redirect_uri='https://www.google.com')
        self.spotify = spotipy.Spotify(auth=self.token,requests_session=True)
        self.monitorW = monitorW
        self.monitorH = monitorH


    def getCurrentImage(self):

        currentTrack = self.spotify.current_playback()
        imageUrl = currentTrack['item']['album']['images'][0]['url']

        image = requests.get(imageUrl)

        img = Image.open(BytesIO(image.content))
        return img


    def createWallpaper(self,img):

        monitorW = self.monitorW
        monitorH = self.monitorH

        imgSize = img.size
        aspectRatio = imgSize[0] / imgSize[1]
        size2 = int(monitorW * aspectRatio)
        img2 = img.resize((monitorW, size2))
        newSize = (monitorW, monitorH)
        mask = Image.new('L', (monitorW, size2), 0)
        draw = ImageDraw.Draw(mask)

        img2.paste(img, (int((newSize[0] - imgSize[0]) / 2), int((size2 - imgSize[1]) / 2)))

        x1 = (monitorW / 2 - imgSize[0] / 2)
        x2 = (monitorW / 2 + imgSize[0] / 2 - 1)
        y1 = (size2 / 2 - imgSize[1] / 2)
        y2 = (size2 / 2 + imgSize[1] / 2 - 1)

        draw.rectangle([(x1, y1), (x2, y2)], fill=255)

        blurred = img2.filter(ImageFilter.GaussianBlur(radius=20))
        blurred.paste(img2, mask=mask)

        blurred = blurred.crop((0, size2 / 2 - monitorH / 2, monitorW, size2 / 2 + monitorH / 2))
        blurred.save("wp.png")
        return blurred

    def currentTrack(self):
        if json.dumps(self.spotify.current_playback()) is not 'null':
            return self.spotify.current_playback()['item']['album']['images'][0]['url']
        else :
            #print("hi")
            return 'null'

    def goodbye(self):
        currentPath = os.path.dirname(os.path.realpath(__file__))
       # ctypes.windll.user32.SystemParametersInfoW(20, 0, currentPath + "\\ogImg.png", 0)

