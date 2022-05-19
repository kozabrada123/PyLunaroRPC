import random
import re
import time

import colorama
import pyautogui
import keyboard
import string

import pytesseract

import lunaroplayers

import cv2
import easyocr

import numpy as np

import settings


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

    #Pretty deprecated

    screenshot = None
    sun = None
    moon = None


    #Hah nft comedy
    nft = param.lower()

    if nft == "sun":

        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 - (800/1920)*pyautogui.size()[0], (450/1080)*pyautogui.size()[1], (250/1920)*pyautogui.size()[0], (250/1080)*pyautogui.size()[1]))

    elif nft == "moon":

        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 + (212/1920)*pyautogui.size()[0], (450/1080)*pyautogui.size()[1], (250/1920)*pyautogui.size()[0], (250/1080)*pyautogui.size()[1]))


    if nft == "suns":

        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 - (580/1920)*pyautogui.size()[0], (240/1080)*pyautogui.size()[1], (150/1920)*pyautogui.size()[0], (70/1080)*pyautogui.size()[1]))


    elif nft == "moons":

        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 + (430/1920)*pyautogui.size()[0], (240/1080)*pyautogui.size()[1], (150/1920)*pyautogui.size()[0], (70/1080)*pyautogui.size()[1]))



    if nft == "time":

        screenshot = pyautogui.screenshot(region=(pyautogui.size()[0] / 2 - (22 / 1920) * pyautogui.size()[0], (94 / 1080) * pyautogui.size()[1], (43 / 1920) * pyautogui.size()[0], (18 / 1080) * pyautogui.size()[1]))

    if nft not in ["sun", "moon", "moons", "suns", "time"]:

        sun = pyautogui.screenshot(region=(pyautogui.size()[0]/2 - 800, 450, 250, 250))

        moon = pyautogui.screenshot(region=(pyautogui.size()[0]/2 + 212, 450, 250, 250))


    settings.console.log(f"Screenshotted {nft}")


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





def getPlayers(args=None, ascreenshot = None, s1 = None, s2 = None, s3 = None, m1 = None, m2 = None, m3 = None):

    if settings.ocr_solution == "easyocr":
        reader = easyocr.Reader(['en'])


        text = reader.readtext(ascreenshot)

        # print(text)

        fa = []

        # Try to run it through the database aswell

        ftext = f""
        for player in text:
            p = lplayers.TryFindByName(player[1])
            if p is not None:
                fa.append(p[1])

        ftext += str(fa).replace("[", "").replace("]", "").replace("'", "")
        #print(ftext)
        settings.console.log(f"[yellow] Found {args} Players! [/yellow]")
        return ftext


    elif settings.ocr_solution == "tesseract":

        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path

        text = pytesseract.image_to_string(image=ascreenshot)
        text = text.split('\n')

        # print(text)

        fa = []

        # Try to run it through the database aswell

        ftext = f""
        for player in text:
            p = lplayers.TryFindByName(player)
            if p is not None:
                fa.append(p[1])

        ftext += str(fa).replace("[", "").replace("]", "").replace("'", "")
        # print(ftext)
        settings.console.log(f"[yellow] Found {args} Players! [/yellow]")
        return ftext



def scoreFilter(char):
    try:
        int(char)
        return True

    except:
        if char != "-":
            return False

        return True



def getScore(args=None, ascreenshot = None):



    if settings.ocr_solution == "easyocr":

        reader = easyocr.Reader(['en'])


        #ascreenshot.save("b.png")

        text = reader.readtext(ascreenshot)

        try:
            #settings.console.log(f"[yellow] {args} Score: {text[0][1]} [/yellow]")
            return [int(text[0][1].split('-')[0]), int(text[0][1].split('-')[1])]
        except:
            return 0

    elif settings.ocr_solution == "tesseract":

        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path


        text = pytesseract.image_to_string(ascreenshot, config='--psm 13')

        #settings.console.log(text)

        try:

            text = ''.join(filter(scoreFilter, text))


            return [int(text.split('-')[0]), int(text.split('-')[1])]
        except:
            return 0


def getEndTimeEpoch(time_screenshot_array):

    if settings.ocr_solution == "easyocr":

        reader = easyocr.Reader(['en'])
        text = reader.readtext(time_screenshot_array)


        m_s = text[0][1].split(".")

        secs = int(m_s[1]) - 1 # -1 since we spend ~a second calculating this

        secs += int(m_s[0]) * 60


        settings.console.log(f"[cyan]Remaining time: {text[0][1]} ({str(secs)} seconds, {str(int(time.time() + secs))})[/cyan]")

        return int(time.time()) + secs



    elif settings.ocr_solution == "tesseract":

        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path

        text = pytesseract.image_to_string(time_screenshot_array, config="--psm 13")

        #print(text)


        m_s = text.split(":")

        secs = int(m_s[1]) - 1 # -1 since we spend ~a second calculating this

        secs += int(m_s[0]) * 60


        settings.console.log(f"[cyan]Remaining time: {text} ({str(secs)} seconds, {str(int(time.time() + secs))})[/cyan]")

        return int(time.time()) + secs




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