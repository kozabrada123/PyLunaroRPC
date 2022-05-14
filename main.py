from queue import Queue
from threading import Thread

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


def update_status(out_queue):
    sun = f"{imrec.getPlayers('sun')}"
    moon = f"{imrec.getPlayers('moon')}"
    pres.updatePresence(sun, moon)
    print("Updated Status!")
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
        time.sleep(1/10)




def continuously_update_status(out_queue):
    pres.updatePresence("Outside of game..", "")
    out_queue.put(["Outside of game..", ""])

    keyboard.add_hotkey(f'Tab+{settings.hotkey}', lambda: update_status(out_queue))
    keyboard.wait()


q = Queue()

t1 = Thread(target = keep_status_alive, args =(q, ))
t2 = Thread(target = continuously_update_status, args =(q, ))

t3 = Thread(target = run_callbacks,)

t1.start()
t2.start()

t3.start()