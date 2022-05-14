import random

import pyautogui
import keyboard
import string
import lunaroplayers



import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'Dependencies/Tesseract-OCR/tesseract.exe'
hotkey = 'o'

lplayers = lunaroplayers.LunaroPlayers()

def screenshot(param="None", save=True):
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


def getSunPlayers():

    text = pytesseract.image_to_string(screenshot("sun"))

    #Try to run it through the database aswell
    try:
        ftext = f"S:"
        fa = []
        for player in text.split():
            fa.append(lplayers.TryFindByName(player)['Shortn'])
        ftext += str(fa).replace("[", "").replace("]", "").replace("'","")
        return ftext
    except:
        return text



def getMoonPlayers():

    text = pytesseract.image_to_string(screenshot("moon"))


    #Try to run it through the database aswell
    try:
        ftext = f"M:"
        fa = []
        for player in text.split():
            fa.append(lplayers.TryFindByName(player)['Shortn'])
        oftext += str(fa).replace("[", "").replace("]", "").replace("'","")
        return ftext
    except:
        return text


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
