<p align="center">
 <img style="display: block; margin-left: auto; margin-right: auto; width:30%;" src="https://raw.githubusercontent.com/kozabrada123/PyLunaroRPC/main/assets/images/Lunaro-logo.png" alt="project logo" width="30%"/>
 </p>

<h2 align="center"> PyLunaroRPC </h2>

A simple tool for Lunaro in Warframe which shows current match data on your profile with Discord RPC.

<br/>

![GitHub](https://img.shields.io/github/license/kozabrada123/PyLunaroRPC?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/kozabrada123/PyLunaroRPC?style=for-the-badge)
![Github Commit Activity m](https://img.shields.io/github/commit-activity/m/kozabrada123/PyLunaroRPC?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/kozabrada123/PyLunaroRPC?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/kozabrada123/PyLunaroRPC?style=for-the-badge)
![LOC](https://img.shields.io/tokei/lines/github/kozabrada123/PyLunaroRPC?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/kozabrada123/PyLunaroRPC?style=for-the-badge)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/kozabrada123/PyLunaroRPC?style=for-the-badge)

<br/>


![No Windows Binaries](https://raw.githubusercontent.com/kozabrada123/PyLunaroRPC/44d0c6136a4a18850e5776e89010a690f6891714/assets/images/no-windows-binaries.svg)
![Lunaro](https://raw.githubusercontent.com/kozabrada123/PyLunaroRPC/98189fcc19354dd62ea8f43dc8d8ad4ef6d6f41b/assets/images/lunaro.svg)

<br/>

- [PyLunaroTracker](#PyLunaroTracker)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [Troubleshooting](#troubleshooting-and-common-issues)
 - [Todo](#to-do-and-future-updates-to-excpect)



## Prerequisites

* Python 3.7+
* Discord
* Warframe to play lunaro

<br/>

* **Currently running on Linux is a bit of a pain, because Keyboard needs Sudo**

## Getting Started

- First, download or git clone this repo.
- Install the python requirements with `pip3 -r requirements.txt`.
- You're done!

## Usage:

- Start the program with `python3 main.py` (or `python main.py`)
- (**Make sure to launch LunaroRPC before Warframe**)
- Launch Warframe
- Go into a game of lunaro
- Press 'o' (default hotkey, configurable in settings.py) while holding TAB
- If nothing broke, game info should be processed and displayed on your profile.

## Troubleshooting and common issues:


- `CUDA not available - defaulting to CPU. Note: This module is much faster with a GPU.` - The most common issue, you can install [Nvidia CUDA](https://developer.nvidia.com/cuda-toolkit) to silence this error and make LunaroRPC run much faster. (Side note: many people may have problems installing CUDA, try to refer to [this](https://forums.developer.nvidia.com/t/windows-10-cuda-installation-failure-solved/64389)) 

- `No package .. was found` - This means one of your requirements isn't properly installed.


- If it doesn't show Lunaro as a running game on Discord, try turning game activity on and off.


- Discord SDK Error 4 - this is an **internal server error on Discord's servers**. Usually, LunaroRPC keeps working.

- Problems with requirements - There might be a mismatch between your python and pip. Try running `python3 -m pip install -r requirements.txt` or `python -m pip install -r requirements.txt`.


## TO-DO And Future Updates To Expect

- Update to use tesseract

- Local Statistics

- **At least basic UI** (Probably gonna be made with [Textual](https://github.com/Textualize/textual))

- Website with statistic tracking per play and leaderboards (Very far future)

- Windows binary (Almost never, hahaha)

