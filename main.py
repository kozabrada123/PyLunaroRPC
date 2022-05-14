from queue import Queue
from threading import Thread

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


def update_status(out_queue):
    sun = f"{imrec.getSunPlayers()}"
    moon = f"{imrec.getMoonPlayers()}"
    pres.updatePresence(sun, moon)
    print("Updated Status!")
    out_queue.put([sun, moon])



def keep_status_alive(in_queue):
    sun = None
    moon = None
    while True:
        try:
            sunnmoon = in_queue.get()
            sun = sunnmoon[0]
            moon = sunnmoon[1]
        except:
            pass

        if not (sun == None or moon == None):
            pres.updatePresence(sun, moon)
        time.sleep(15)


def continuously_update_status(out_queue):
    pres.updatePresence("Outside of game..", None)
    out_queue.put(["Outside of game..", None])

    keyboard.add_hotkey(settings.hotkey, lambda: update_status(out_queue))
    keyboard.wait()


q = Queue()

t1 = Thread(target = keep_status_alive, args =(q, ))
t2 = Thread(target = continuously_update_status, args =(q, ))

t1.start()
t2.start()