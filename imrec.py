import random

import pyautogui
import keyboard
import string
import lunaroplayers

import cv2
import easyocr

import numpy as np


#import pytesseract

#pytesseract.pytesseract.tesseract_cmd = r'Dependencies/Tesseract-OCR/tesseract.exe'
hotkey = 'o'

lplayers = lunaroplayers.LunaroPlayers()

def screenshot(param="None", save=False):
    """
    Screenshots the screen.
    :param str nft: "Sun 1-3" or "Moon 1-3"
    :param bool save: Whether to save as a file or not
    :return: pyautogui image
    """

    screenshot = None
    sun = None
    moon = None


    #Hah nft comedy
    nft = param.lower()

    if nft == "sun":
        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 - 800, 450, 250, 250))

    elif nft == "moon":
        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 + 212, 450, 250, 250))




    if nft not in ["sun", "moon", "sun1", "sun2", "sun3", "moon1", "moon2", "moon3"]:
        sun = pyautogui.screenshot(region=(pyautogui.size()[0]/2 - 800, 450, 250, 250))

        moon = pyautogui.screenshot(region=(pyautogui.size()[0]/2 + 212, 450, 250, 250))


    if save:
        try:
            screenshot.save("debug.png")
        except:
            try:
                a = str(random.randint(0, 100000))
                print(a)
            except:
                pass


    if sun == None and moon == None:
        return screenshot
    else:
        return sun, moon





def getPlayers(args=None, ascreenshot = None):

    if args == "moon":

        reader = easyocr.Reader(['en'])
        if ascreenshot == None:
            ascreenshot = screenshot("moon")

        text = reader.readtext(np.array(ascreenshot))
        #print(text)
        fa = []

        #Try to run it through the database aswell

        ftext = f"🌙: "
        for player in text:
            fa.append(lplayers.TryFindByName(player[1])[1])
        ftext += str(fa).replace("[", "").replace("]", "").replace("'","")
        #print(ftext)
        return ftext


    if args == "sun":

        reader = easyocr.Reader(['en'])

        if ascreenshot == None:
            ascreenshot = screenshot("sun")

        text = reader.readtext(np.array(ascreenshot))

        # print(text)

        fa = []

        # Try to run it through the database aswell

        ftext = f"☀️: "
        for player in text:
            fa.append(lplayers.TryFindByName(player[1])[1])
        ftext += str(fa).replace("[", "").replace("]", "").replace("'", "")
        #print(ftext)
        return ftext

    else:
        return None


def wait(debug=False):
    """
    Waits until hotkey pressed and then screenshots
    :return: Screenshot
    """
    while not keyboard.is_pressed(hotkey):
        pass

    if debug:
        return screenshot(save=True)
    else:
        return screenshot()
