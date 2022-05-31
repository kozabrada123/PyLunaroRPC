from queue import Queue, PriorityQueue
from threading import Thread

import asyncio

from PIL import Image

import colorama

import numpy as np

import cv2
import pyautogui

import settings

import time

import keyboard

import imrec
import presence

_sentinel = object()

sun = None
moon = None

pres = presence.presenceManager()
pres.startPresence()


def managePresence(player_queue, score_queue):


    player_queue_old = ["", ""]
    score_queue_old = [-1, -1]


    time.sleep(1)


    while True:

        try:

            # First check if score is messed up
            cplayer_queue = player_queue.queue[0]
            cscore_queue = score_queue.queue[0]

            # (Sun)
            # If score has increased by more than 3, we've done an oopsie
            if (cscore_queue[0] - score_queue_old[0]) > 3:
                # If we read it falsely, fallback to old value
                cscore_queue[0] = score_queue_old[0]

            # Now with moon as well
            if (cscore_queue[1] - score_queue_old[1]) > 3:
                cscore_queue[1] = score_queue_old[1]

            # Score should now be fine

            # Check if player queue is messed up

            # (Sun)
            # If any queue is "" it means we did a shit
            if cplayer_queue[0] == "":
                cplayer_queue[0] = player_queue_old[0]

            # Now with moon as well
            # If any queue is "" it means we did a shit
            if cplayer_queue[1] == "":
                cplayer_queue[1] = player_queue_old[1]

            # Fixing is done, update stuff

            # If nothing changed, don't do anything
            if player_queue_old == cplayer_queue and score_queue_old == cscore_queue:

                # Exception stops update and nothing happens because of try except
                raise Exception("No update needed, passing update")

            # Update everything, even if it hasn't changed, just so we have a lot of if statements
            pres.update_status(sun_players=cplayer_queue[0],
                               moon_players=cplayer_queue[1],
                               sun_score=cscore_queue[0],
                               moon_score=cscore_queue[1]
                               )

            #Set old queue to new queue
            player_queue_old = cplayer_queue
            score_queue_old = cscore_queue

        except:
            pass

        time.sleep(0.2)

        #print(player_queue.queue, score_queue.queue)

def run_callbacks():
    while 1:
        time.sleep(1/10)
        pres.runCallbacks()


def update_players(out_queue):


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
    #Now calculating the score a different way.
    #suns_left = pyautogui.size()[0]/2 - (580/1920)*pyautogui.size()[0]#x
    #suns_upper = (240/1080)*pyautogui.size()[1]#y
    #suns_right = suns_left + (150/1920)*pyautogui.size()[0]#x + width
    #suns_lower = suns_upper + (70/1080)*pyautogui.size()[1]#y + height

    #suns_screenshot = screenshot.crop((suns_left, suns_upper, suns_right, suns_lower))

    #suns_screenshot.save("ss.png")


    #moons_left = pyautogui.size()[0]/2 + (430/1920)*pyautogui.size()[0]#x
    #moons_upper = (240/1080)*pyautogui.size()[1]#y
    #moons_right = moons_left + (150/1920)*pyautogui.size()[0]#x + width
    #moons_lower = moons_upper + (70/1080)*pyautogui.size()[1]#y + height

    #moons_screenshot = screenshot.crop((moons_left, moons_upper, moons_right, moons_lower))

    #moons_screenshot.save("mns.png")



    #if settings.auto:
    #    keyboard.release("Tab")

    settings.console.log("[green] Safe to close tab.. [/green]")

    sun_players = imrec.getPlayers('sun', np.array(sun_screenshot))

    moon_players = imrec.getPlayers('moon', np.array(moon_screenshot))



    out_queue.queue[0] = [sun_players, moon_players]



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




def continuously_update_status(out_queue):
    #print(f"{colorama.Fore.CYAN}Outside of Game")
    settings.console.log(f"[cyan] Outside of game.. [/cyan]")
    out_queue.queue.append(["Outside of game..", ""])

    keyboard.add_hotkey(f'Tab', lambda: update_players(out_queue))
    keyboard.wait()


def fetch_time(score_queue):
    score_queue.put([0, 0])
    while True:



        #try:
        screenshot = pyautogui.screenshot("t.png")
        screenshot = Image.open("t.png")

        time_left = pyautogui.size()[0] / 2 - (22 / 1920) * pyautogui.size()[0]  # x
        time_upper = (90 / 1080) * pyautogui.size()[1]  # y
        time_right = time_left + ((43 / 1920) * pyautogui.size()[0])  # x + width
        time_lower = time_upper + ((25 / 1080) * pyautogui.size()[1])  # y + height

        time_screenshot = screenshot.crop((time_left, time_upper, time_right, time_lower))
        #time_screenshot.save("ts.png")


        score_left = pyautogui.size()[0] / 2 - (75 /1920) * pyautogui.size()[1] # x
        score_upper = (60 / 1080) * pyautogui.size()[1]
        score_right = score_left + ((80 / 1920) * pyautogui.size()[0]) #x + width
        score_lower = score_upper + ((55 / 1920) * pyautogui.size()[1]) #y + height

        score_screenshot = screenshot.crop((score_left, score_upper, score_right, score_lower)).convert("L")
        score_screenshot = cv2.fastNlMeansDenoising(np.array(score_screenshot), None, 10, 7, 21)
        score_screenshot = Image.fromarray(score_screenshot)
        score_screenshot = score_screenshot.resize([score_screenshot.size[0] * 2, score_screenshot.size[1] * 2])

        score_screenshot.save("s.png")



        try:
            ss, sm = imrec.getScore("sun and moon", np.array(score_screenshot))
            score_queue.queue[0] = [ss, sm]
            #print(str(score_queue.queue))
        except: pass
            #print(e)

        try:
            endt = imrec.getEndTimeEpoch(np.array(time_screenshot))
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



        time.sleep(2)
        # only need get time every 2s



#General queue
player_queue = PriorityQueue()

#Time queues
score_queue = PriorityQueue()


#score_queue.put([0,0])

#t1 = Thread(target = keep_status_alive, args =(player_queue, ))

player_queue.queue.append(["", ""])
score_queue.queue.append([-1, -1])

tabt = Thread(target = continuously_update_status, args =(player_queue, ))
callt = Thread(target = run_callbacks)
timet = Thread(target = fetch_time, args=(score_queue, ))
mngt = Thread(target = managePresence, args=(player_queue, score_queue, ))

#t1.start()


tabt.start()
callt.start()
timet.start()
mngt.start()