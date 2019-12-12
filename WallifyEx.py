import Wallify
import os
import sys
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from json.decoder import JSONDecodeError
import ctypes
from io import BytesIO
import requests
from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
import time
import subprocess
import atexit
import winreg
import time

aReg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)

user32 = ctypes.windll.user32
monitorW = user32.GetSystemMetrics(0)
monitorH = user32.GetSystemMetrics(1)

start_time = time.time()
firstTime = True
wallify = Wallify.Wallify(monitorW,monitorH)
currentTrack = wallify.currentTrack()
currentPath = os.path.dirname(os.path.realpath(__file__))
atexit.register(wallify.goodbye)
key = winreg.OpenKey(aReg,'Software\Microsoft\Windows\CurrentVersion\Explorer\Wallpapers')
print(winreg.QueryValueEx(key, "BackgroundHistoryPath0")[0])
ogImg = Image.open(winreg.QueryValueEx(key, "BackgroundHistoryPath0")[0])
ogImg.save("ogImg.png")
atexit.register(wallify.goodbye)

print("Exit this program using Ctrl + C in the console, failing to do so will result in you old wallpaper not being reset")

try:
    while True:
        try:
            if(json.dumps(wallify.currentTrack()) is not 'null'):
                oldTrack = currentTrack
                currentTrack = wallify.currentTrack()
                if wallify.currentTrack() != oldTrack or firstTime == True:
                    albumCover = wallify.getCurrentImage()
                    wallpaper = wallify.createWallpaper(albumCover)
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, currentPath + "\\wp.png", 0)
                    firstTime = False

                else:
                    currentTrack = oldTrack
            else:
                time.sleep(1)

            if(time.time() - start_time > 600):
                wallify = Wallify.Wallify(monitorW, monitorH)
                start_time = time.time()
        except KeyboardInterrupt:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, currentPath + "\\ogImg.png", 0)
            sys.exit()
        except:
            time.sleep(2)

finally:
   print("Bye")




