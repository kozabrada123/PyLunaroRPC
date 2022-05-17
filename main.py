from queue import Queue
from threading import Thread

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
    #wait 0.2s for tab to load
    time.sleep(0.2)

    #Start time updating
    tstart_queue.put(True)

    sun_screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 - (800/1920)*pyautogui.size()[0], (450/1080)*pyautogui.size()[1], (250/1920)*pyautogui.size()[0], (250/1080)*pyautogui.size()[1]))

    moon_screenshot = pyautogui.screenshot(region=(pyautogui.size()[0]/2 + (212/1920)*pyautogui.size()[0], (450/1080)*pyautogui.size()[1], (250/1920)*pyautogui.size()[0], (250/1080)*pyautogui.size()[1]))

    #+s == Score
    suns_screenshot =  pyautogui.screenshot(region=(pyautogui.size()[0]/2 - (580/1920)*pyautogui.size()[0], (240/1080)*pyautogui.size()[1], (150/1920)*pyautogui.size()[0], (70/1080)*pyautogui.size()[1]))

    moons_screenshot =  pyautogui.screenshot(region=(pyautogui.size()[0]/2 + (430/1920)*pyautogui.size()[0], (240/1080)*pyautogui.size()[1], (150/1920)*pyautogui.size()[0], (70/1080)*pyautogui.size()[1]))


    settings.console.log("[green] Safe to close tab.. [/green]")

    sun = f"☀️ {imrec.getScore('sun', np.array(suns_screenshot))}: {imrec.getPlayers('sun', np.array(sun_screenshot))}"
    moon = f"🌙 {imrec.getScore('moon', np.array(moons_screenshot))}: {imrec.getPlayers('moon', np.array(moon_screenshot))}"
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


def fetch_time(start_queue):
    while True:
        #if start_queue.get == True:
        if True:
            try:
                tscreenshot = pyautogui.screenshot(region=(pyautogui.size()[0] / 2 - (22 / 1920) * pyautogui.size()[0], (94 / 1080) * pyautogui.size()[1], (43 / 1920) * pyautogui.size()[0], (18 / 1080) * pyautogui.size()[1]))



                endt = imrec.getEndTimeEpoch(np.array(tscreenshot))

                pres.updateTime(endt)


            except: pass

            time.sleep(5)
            #only need get time every 2s



#General queue
q = Queue()

#Time queues
tstart_queue = Queue()

q.put(["", ""])

t1 = Thread(target = keep_status_alive, args =(q, ))
t2 = Thread(target = continuously_update_status, args =(q, tstart_queue, ))


t3 = Thread(target = run_callbacks)
timet = Thread(target = fetch_time, args=(tstart_queue, ))

t1.start()
t2.start()

t3.start()
timet.start()

