from queue import Queue
from threading import Thread

import colorama

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
    sun_screenshot = imrec.screenshot("sun")
    moon_screenshot = imrec.screenshot("moon")

    #+s == Score
    suns_screenshot = imrec.screenshot("suns")
    moons_screenshot = imrec.screenshot("moons")

    sun = f"☀️ {imrec.getScore('sun', suns_screenshot)}: {imrec.getPlayers('sun', sun_screenshot)}"
    moon = f"🌙 {imrec.getScore('moon', moons_screenshot)}: {imrec.getPlayers('moon', moon_screenshot)}"
    pres.updatePresence(sun, moon)
    #print("Updated Status!")
    #print(f"{colorama.Fore.CYAN}{moon}; {colorama.Fore.YELLOW}{sun}")
    settings.console.log(f"[cyan bold]{colorama.Fore.CYAN}{moon.replace('🌙','🌙 Moon')} [/cyan bold][yellow bold]{colorama.Fore.YELLOW}{sun.replace('☀️ ', '☀ Sun ')}[/yellow bold]")
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
    #print(f"{colorama.Fore.CYAN}Outside of Game")
    settings.console.log(f"[cyan]{colorama.Fore.CYAN} Outside of game.. [/cyan]")
    pres.updatePresence("Outside of game..", "")
    out_queue.put(["Outside of game..", ""])

    keyboard.add_hotkey(f'Tab+{settings.hotkey}', lambda: update_status(out_queue))
    keyboard.wait()


q = Queue()

q.put(["", ""])

t1 = Thread(target = keep_status_alive, args =(q, ))
t2 = Thread(target = continuously_update_status, args =(q, ))

t3 = Thread(target = run_callbacks)


t1.start()
t2.start()

t3.start()

