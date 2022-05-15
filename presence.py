import threading
import time
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



    def startPresence(self):
        self.app = dsdk.Discord(settings.appid, dsdk.CreateFlags.default)
        self.RPC_Manager = self.app.get_activity_manager()


        self.RPC = dsdk.Activity()
        self.RPC.details = f"{self.sun}"
        self.RPC.state = f"{self.moon}"
        self.RPC.assets.small_image = "https://i.ibb.co/f4xwkTm/Lunaro-logo-pog.png"

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


    def runCallbacks(self):
        self.app.run_callbacks()


    def debugCallback(self, result, something=None):
        if result == dsdk.Result.ok:
            #print("Successfully set the activity!")
            pass
        else:
            #print(result)
            pass

    def stop(self):
        self.RPC.close()
        self.RPC = ""
