# Standard python libs
import importlib 
import subprocess
import tkinter as tk
import json
import webbrowser
import time
# VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
installedlibs = False # Please change it to True later!
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
required_libraries = ['pyautoit', 'keyboard',"opencv-python", 'pyautogui', 'pillow']

missing_libraries = []
if installedlibs == False:

    for library in required_libraries:
     try:
        importlib.import_module(library)
     except ImportError:
        missing_libraries.append(library)

if missing_libraries:
    print("Installing needed libraries...")
    for library in missing_libraries:
        subprocess.check_call(['pip', 'install', library])
else:
    print("All required libraries are already installed.")

# Required imports
import autoit
import keyboard as key
import pyautogui



root = tk.Tk()

# dark mode
root.configure(bg='black')
root.tk_setPalette(background='black', foreground='white')


# variables for the settings
Viplink = tk.StringVar()
LoadingWaitTime = tk.IntVar()

# function to load settings from the JSON file
def load_settings():
    try:
        with open("settingsnodiscord.json", "r") as file:
            settings = json.load(file)
            Viplink.set(settings.get("Viplink", ""))
            LoadingWaitTime.set(settings.get("LoadingWaitTime", 0))
    except FileNotFoundError:
        pass


# function to save settings to the JSON file
def submit():
    global Viplink, LoadingWaitTime, webhooklink, client_id, discordid
    Viplink = entry_viplink.get()
    LoadingWaitTime = int(entry_loadingtime.get())
    
    # save the settings to a JSON file
    settings = {
        "Viplink": Viplink,
        "LoadingWaitTime": LoadingWaitTime,
    }
    
    with open("settingsnodiscord.json", "w") as file:
        json.dump(settings, file)
    
    root.destroy()


load_settings()

# settings gui
label_viplink = tk.Label(root, text="Viplink:", bg="black", fg="white")
label_viplink.pack()
entry_viplink = tk.Entry(root, textvariable=Viplink, bg="black", fg="white")
entry_viplink.pack()

label_loadingtime = tk.Label(root, text="Loading Wait Time:", bg="black", fg="white")
label_loadingtime.pack()
entry_loadingtime = tk.Entry(root, textvariable=LoadingWaitTime, bg="black", fg="white")
entry_loadingtime.pack()


# ability to move the window
def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

# bind the function to the title bar
root.overrideredirect(True)
root.title("Settings")
root.bind('<B1-Motion>', move_window)

# submit button
submit_button = tk.Button(root, text="Submit", command=submit, bg="black", fg="white")
submit_button.pack()

root.mainloop()


TotalRounds = 0


def UpdateTotal():
    global TotalRounds
    TotalRounds += 1

    
def JoinVip():
    webbrowser.open(Viplink)
    playbutton = pyautogui.locateOnScreen('Play.png', confidence=0.5)
    while True:
        time.sleep(1)
        time.sleep(LoadingWaitTime)
        if playbutton is not None:
            print("I can see it")
            autoit.mouse_click("left", x=157, y=482) # Play
            time.sleep(1)
            key.press("a")
            key.press("space")
            time.sleep(10) # can do longer if ur internet slow
            key.release("a")
            key.release("space")
            break
        else: 
            print("can't find play button")
            continue
        

def CheckIfDisconnected():
    disconnectedimg = pyautogui.locateOnScreen('Disconnected.png', confidence=0.6)
    if disconnectedimg is not None:
        print("disconnected in game")
        LobbyMacro()
    
    
def CheckIfJoinedGame():
    votebutton = None
    while votebutton is None:
        CheckIfDisconnected()
        time.sleep(3)
        votebutton = pyautogui.locateOnScreen('Vote.png', confidence=0.7)
        print("I can see vote button.")
    autoit.mouse_click("left", x=921, y=174) # Start game (yes button)



def Restart():
        autoit.mouse_click("left", x=765, y=720) # Next button
        autoit.mouse_click("left", x=769, y=720) # 1
        autoit.mouse_click("left", x=766, y=720) # -  Clicking 3 times to claim rewards (aka fruits idk)
        time.sleep(1)
        autoit.mouse_click("left", x=767, y=720) # 3
        autoit.mouse_click("left", x=1108, y=218) # Replay button


def CheckIfLost():
    NextButton = None
    while NextButton is None:
        time.sleep(3)
        NextButton = pyautogui.locateOnScreen("Lost.png", confidence=0.7)


def LobbyMacro():
    JoinVip()
    GameMacro()
    
    
def GameMacro():
    while True:
        # autoit.mouse_click("left", x=921, y=174) # Start game (yes button)
        CheckIfJoinedGame()
        CheckIfLost()
        UpdateTotal()
        Restart()    
        
        
LobbyMacro()