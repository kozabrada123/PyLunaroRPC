import threading
import time

import numpy as np
import pyautogui
from PIL.Image import Image

import imrec
import settings

import discordsdk as dsdk

import pypresence

class presenceManager:
    def __init__(self):
        self.RPC = None
        self.app = None
        self.RPC_Manager = None
        self.sun = ""
        self.moon = ""

        self.sun_players = ""
        self.moon_players = ""
        self.sun_score = 0
        self.moon_score = 0





    def startPresence(self):
        self.app = dsdk.Discord(settings.appid, dsdk.CreateFlags.default)
        self.RPC_Manager = self.app.get_activity_manager()


        self.RPC = dsdk.Activity()
        self.RPC.details = f"{self.sun}"
        self.RPC.state = f"{self.moon}"
        self.RPC.assets.small_image = "https://raw.githubusercontent.com/kozabrada123/PyLunaroRPC/main/assets/images/Lunaro-logo.png"

        self.RPC_Manager.update_activity(self.RPC, lambda result: self.debugCallback("update_activity", result))


    def restartPresence(self):

        self.RPC_Manager = self.app.get_activity_manager()

        self.RPC = dsdk.Activity()
        self.RPC.details = f"{self.sun}"
        self.RPC.state = f"{self.moon}"
        self.RPC.assets.small_image = "https://raw.githubusercontent.com/kozabrada123/PyLunaroRPC/main/assets/images/Lunaro-logo.png"

        self.RPC_Manager.update_activity(self.RPC, lambda result: self.debugCallback("update_activity", result))



    def updatePresence(self, sun, moon):
        self.sun = sun
        self.moon = moon

        try:
            #self.RPC.update(small_image="https://i.ibb.co/f4xwkTm/Lunaro-logo-pog.png", details=sun, state=moon)
            self.RPC.details = self.sun
            if self.moon != "":
                self.RPC.state = self.moon
        except:
            self.RPC.details = f"{self.sun}"
            if self.moon != "":
                self.RPC.state = f"{self.moon}"
            #self.RPC.update(small_image="https://i.ibb.co/f4xwkTm/Lunaro-logo-pog.png", details=f"{sun}, {moon}")

        self.RPC_Manager.update_activity(self.RPC, self.debugCallback)




    def update_status(self, sun_players=None, moon_players=None, sun_score=None, moon_score=None):


        if sun_players is not None:
            self.sun_players = sun_players

        if moon_players is not None:
            self.moon_players = moon_players


        if sun_score is not None:
            self.sun_score = sun_score

        if moon_score is not None:
            self.moon_score = moon_score



        sun = f"☀️ {self.sun_score}: {self.sun_players}"
        moon = f"🌙 {self.moon_score}: {self.moon_players}"

        self.updatePresence(sun, moon)
        # print("Updated Status!")
        # print(f"{colorama.Fore.CYAN}{moon}; {colorama.Fore.YELLOW}{sun}")
        settings.console.log(    f"[cyan bold] {moon.replace('🌙', '🌙 Moon')} [/cyan bold][yellow bold] {sun.replace('☀️ ', '☀ Sun ')}[/yellow bold]")
        #out_queue.put([sun, moon])


    def updateTime(self, time):
        settings.console.log("Updating time")
        self.endt = time
        self.RPC.timestamps.end = self.endt

        self.RPC_Manager.update_activity(self.RPC, self.debugCallback)


    def runCallbacks(self):
        try:
            self.app.run_callbacks()
        except:
            try:
                self.restartPresence()
                self.update_status()
            except:
                print("Discord SDK Broke..")



    def debugCallback(self, result, something=None):
        if result == dsdk.Result.ok:
            #print("Successfully set the activity!")
            pass
        else:

            if result == dsdk.Result.internal_error:
                # Restart
                print("Restarting...")

                try:
                    self.restartPresence()
                    self.update_status()
                except: pass

    def stop(self):
        self.RPC.close()
        self.RPC = ""
