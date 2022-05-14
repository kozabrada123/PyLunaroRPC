# PyLunaroTracker
A simple tool for Warframe Lunaro which shows players in the match on your profile with Discord RPC.

![GitHub](https://img.shields.io/github/license/kozabrada123/PyLunaroTracker)
![GitHub top language](https://img.shields.io/github/languages/top/kozabrada123/PyLunaroTracker)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/kozabrada123/PyLunaroTracker)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kozabrada123/PyLunaroTracker)
![GitHub issues](https://img.shields.io/github/issues/kozabrada123/PyLunaroTracker)
![GitHub last commit](https://img.shields.io/github/last-commit/kozabrada123/PyLunaroTracker)
![LOC](https://img.shields.io/tokei/lines/github/kozabrada123/PyLunaroTracker)



- [PyLunaroTracker](#PyLunaroTracker)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [Troubleshooting](#troubleshooting-and-common-issues)



## Prerequisites

* Python 3.7+
* **A working install of tesseract** (To be changed in future, for now this makes it only work on Windows)
* Some willingness to mess around with Discord



## Getting Started

- First, download or git clone this repo.
- Install the python requirements with `pip3 install -r requirements.txt`
- Install Tesseract and copy it's folder (usually `C:\Program Files\Tesseract-OCR`) to Dependencies. (File structure should look like `PyLunaroTracker/Dependencies/Tesseract-OCR/tesseract.exe`)
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Create an app called "Warframe: Lunaro" or whatever you want it to be named
- Copy the Application Id of the app
- Go into `presence.py`
- In line 14, `self.RPC = pypresence.Presence(client_id=YOURCLIENTID)`, set `YOURCLIENTID` to the client id from the Discord Developer App you made.
- Everything should now be set up!

## Usage:

- Start the program with `python3 main.py`
- Launch Warframe
- Go into a game of lunaro
- Press 'o' (default hotkey, can be changed) while holding TAB
- If everything is set up correctly, the players from both team should be visible on your profile.

## Troubleshooting and common issues:

- `No package .. was found` - This usually means you haven't installed the requirements correctly, try manually installing the library with pip

- `pytesseract.pytesseract.TesseractNotFoundError: Dependencies/Tesseract-OCR/tesseract.exe is not installed or it's not in your PATH. See README file for more information.` - this means you haven't properly installed Tesseract or it isn't in the right location

- Can't see presence on profile - This usually means you haven't enabled Game Activity in Discord Settings (`Settings/Activity Status/Display current activity as status message`). If you have, try to exit any other running games or try to turn Game Activity On and Off. 


