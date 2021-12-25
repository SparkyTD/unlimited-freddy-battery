# Unlimited Freddy Battery

A small python script that gives you unlimited battery time in [Five Night at Freddy's: Security Breach](https://store.steampowered.com/app/747660/Five_Nights_at_Freddys_Security_Breach/). It works by writing directly into the game's memory, and resetting the battery countdown timer every five seconds. **This is a cheat software, so please only use it after you've already finished the game's main storyline, and fully upgraded your Freddy!**

## Download (no installation)
The latest release can be downloaded [HERE](https://github.com/SparkyTD/unlimited-freddy-battery/releases/download/v1.1/UnlimitedFreddyBattery.v1.1.exe). There's no need to install anything, just run the executable file.

If you do not trust the .exe file, you can also use the python script directly ("Manual Installation" section).

## Manual Installation (advanced)
The executable file provided in the Releases section **works out of the box**. However, if you don't feel comfortable downloading and running a random exe you found on the internet, you can also download the source code itself, and run it directly with python. Here's how you do it:

1. Make sure that [Python 3](https://www.python.org/downloads/) is installed on your computer
2. Open a terminal (press `Win+R`, type `cmd`, enter)
3. Navigate to a directory where you would like to download the script (e.g. `cd C:\Users\Sparky\Downloads`)
4. Clone this repo: `git clone https://github.com/SparkyTD/infinite-freddy-time`
5. Navigate to the downloaded directory: `cd infinite-freddy-time`
6. Install the dependency: `pip install -r requirements.txt`
7. Run the script: `python main.py`
8. You can launch the game before, or after you run the script, it doesn't matter.

## How to use
Using the script is very easy. Just launch the game and run the script. You can also launch the script first, and then the game, the order doesn't matter. As long as the script is running in the background, Freddy's battery will never deplete. When you're done playing, hit `Ctrl+C` in the script's command window to close it.

## I have a problem with the script
Please don't hesitate to open a new Issue in the [Issues](https://github.com/SparkyTD/infinite-freddy-time/issues) tab. Make sure to include as much information as you can about the problem, so it can be fixed faster (Screenshot, Windows version, Game version, etc...).

## Why did my antivirus flag the exe file?
The released executable file is a bundled python script that was made with [pyinstaller](https://www.pyinstaller.org/). Unfortunately there are lots of malwares that use a similar type of packaging, which may cause [some antivirus programs](https://www.virustotal.com/gui/file/47667893eee4c4f5d0b8ad34569eaa8a37c765ec38a3c86482d1eca23ab68e83?nocache=1) to think that this is a virus. To make it even worse, this script works by directly modifying the game's memory, which can also raise some red flags in antivirus softwares. 

This script is completely harmless, it only does what's described on this page, and nothing else. Feel free to inspect the source code, and use the manual installation method if you don't want to run the released executable.

## How exactly does this script work?
The script works by accessing the game's main memory region at offset `"fnaf9-Win64-Shipping.exe"+0x0403AB30`, and following a set of pointers (`0x60 -> 0x9A8 -> 0x240 -> 0x50 -> 0xB8`) to find the uint32 variable that stores Freddy's battery duration in seconds. This number starts from 100 when Freddy gets out of a charging station, and slowly counts down to 0. This script resets this counter to 100

## License
Do whatever you want with this script, but if you want to modify and/or redistribute it, **please include a link to this github page**!
