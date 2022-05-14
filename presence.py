import threading
import time

import pypresence

class presenceManager:
    def __init__(self):
        self.RPC = None
        self.sun = ""
        self.moon = ""


    def startPresence(self):
        self.RPC = pypresence.Presence(client_id=970782366815641620)
        self.RPC.connect()

    def updatePresence(self, sun, moon):
        self.sun = sun
        self.moon = moon

        try:
            self.RPC.update(small_image="https://i.ibb.co/f4xwkTm/Lunaro-logo-pog.png", details=sun, state=moon)
        except:
            self.RPC.update(small_image="https://i.ibb.co/f4xwkTm/Lunaro-logo-pog.png", details=f"{sun}, {moon}")

    def stop(self):
        self.RPC.close()
        self.RPC = "Bongo Cat deep throats very large cock"