from queue import Queue
from threading import Thread

import colorama

import numpy as np

import cv2

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

    sun_screenshot = np.array(imrec.screenshot("sun"))
    moon_screenshot = np.array(imrec.screenshot("moon"))

    #+s == Score
    suns_screenshot = np.array(imrec.screenshot("suns"))
    moons_screenshot = np.array(imrec.screenshot("moons"))

    sun = f"☀️ {imrec.getScore('sun', suns_screenshot)}: {imrec.getPlayers('sun', sun_screenshot)}"
    moon = f"🌙 {imrec.getScore('moon', moons_screenshot)}: {imrec.getPlayers('moon', moon_screenshot)}"
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
                tscreenshot = np.array(imrec.screenshot("time"))


                endt = imrec.getEndTimeEpoch(tscreenshot)

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

