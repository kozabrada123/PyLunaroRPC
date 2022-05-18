from queue import Queue
from threading import Thread

import asyncio

from PIL import Image

import colorama

import numpy as np

import cv2
import pyautogui

import settings

_sentinel = object()

import time

import keyboard

import imrec
import presence


sun = None
moon = None



pres = presence.presenceManager()
pres.startPresence()

def run_callbacks():
    while 1:
        time.sleep(1/10)
        pres.runCallbacks()


def update_status(out_queue, tstart_queue):
    #Start time updating
    tstart_queue.put(True)


    #wait 0.5s for tab to load
    time.sleep(0.5)



    screenshot = pyautogui.screenshot("sc.png")
    screenshot = Image.open("sc.png")



    sun_left = pyautogui.size()[0]/2 - (800/1920)*pyautogui.size()[0]#x
    sun_upper = (450/1080)*pyautogui.size()[1]#y
    sun_right = sun_left + ((250/1920)*pyautogui.size()[0])#x + width
    sun_lower = sun_upper + (250/1080)*pyautogui.size()[1]#y + height

    sun_screenshot = screenshot.crop((sun_left, sun_upper, sun_right, sun_lower))
    #sun_screenshot.save("sn.png")


    moon_left = pyautogui.size()[0]/2 + (212/1920)* pyautogui.size()[0]#x
    moon_upper = (450/1080)*pyautogui.size()[1]#y
    moon_right = moon_left + (250/1920)* pyautogui.size()[0]#x + width
    moon_lower = moon_upper + (250/1080)* pyautogui.size()[1]#y+ height

    moon_screenshot = screenshot.crop((moon_left, moon_upper, moon_right, moon_lower))
    #moon_screenshot.save("mn.png")

    #+s == Score
    suns_left = pyautogui.size()[0]/2 - (580/1920)*pyautogui.size()[0]#x
    suns_upper = (240/1080)*pyautogui.size()[1]#y
    suns_right = suns_left + (150/1920)*pyautogui.size()[0]#x + width
    suns_lower = suns_upper + (70/1080)*pyautogui.size()[1]#y + height

    suns_screenshot = screenshot.crop((suns_left, suns_upper, suns_right, suns_lower))


    moons_left = pyautogui.size()[0]/2 + (430/1920)*pyautogui.size()[0]#x
    moons_upper = (240/1080)*pyautogui.size()[1]#y
    moons_right = moons_left + (150/1920)*pyautogui.size()[0]#x + width
    moons_lower = moons_upper + (70/1080)*pyautogui.size()[1]#y + height

    moons_screenshot = screenshot.crop((moons_left, moons_upper, moons_right, moons_lower))



    #if settings.auto:
    #    keyboard.release("Tab")

    settings.console.log("[green] Safe to close tab.. [/green]")

    sun_players = imrec.getPlayers('sun', np.array(sun_screenshot))

    moon_players = imrec.getPlayers('moon', np.array(moon_screenshot))

    sscore = imrec.getScore('sun', np.array(suns_screenshot))

    mscore = imrec.getScore('moon', np.array(moons_screenshot))



    sun = f"☀️ {sscore}: {sun_players}"
    moon = f"🌙 {mscore}: {moon_players}"
    pres.updatePresence(sun, moon)
    #print("Updated Status!")
    #print(f"{colorama.Fore.CYAN}{moon}; {colorama.Fore.YELLOW}{sun}")
    settings.console.log(f"[cyan bold] {moon.replace('🌙','🌙 Moon')} [/cyan bold][yellow bold] {sun.replace('☀️ ', '☀ Sun ')}[/yellow bold]")
    out_queue.put([sun, moon])



def keep_status_alive(in_queue):
    sun = ""
    moon = ""
    while True:
        try:
            sunnmoon = in_queue.get()
            sun = sunnmoon[0]
            moon = sunnmoon[1]
        except:
            pass

        if not (sun == None or moon == None):
            pres.updatePresence(sun, moon)
        time.sleep(0.2)




def continuously_update_status(out_queue, tstart_queue):
    #print(f"{colorama.Fore.CYAN}Outside of Game")
    settings.console.log(f"[cyan] Outside of game.. [/cyan]")
    pres.updatePresence("Outside of game..", "")
    out_queue.put(["Outside of game..", ""])

    keyboard.add_hotkey(f'Tab', lambda: update_status(out_queue, tstart_queue))
    keyboard.wait()


def fetch_time(gen_queue, start_queue):
    while True:

        if start_queue.get() == True:
            try:
                tscreenshot = pyautogui.screenshot(region=(pyautogui.size()[0] / 2 - (22 / 1920) * pyautogui.size()[0], (94 / 1080) * pyautogui.size()[1], (43 / 1920) * pyautogui.size()[0], (18 / 1080) * pyautogui.size()[1]))



                endt = imrec.getEndTimeEpoch(np.array(tscreenshot))

                pres.updateTime(endt)



            except: pass


            #try:
            #    if settings.auto:
            #        keyboard.press("Tab")
            #        update_status(gen_queue, start_queue)
            #        time.sleep(0.2)
            #        keyboard.release("Tab")
            #except:
            #   pass



            time.sleep(5)
            # only need get time every 5s



#General queue
q = Queue()

#Time queues
tstart_queue = Queue()

q.put(["", ""])

t1 = Thread(target = keep_status_alive, args =(q, ))
t2 = Thread(target = continuously_update_status, args =(q, tstart_queue, ))


t3 = Thread(target = run_callbacks)
timet = Thread(target = fetch_time, args=(q, tstart_queue, ))

t1.start()


t2.start()

t3.start()
timet.start()


