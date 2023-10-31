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
required_libraries = ['pyautoit', 'keyboard', 'discord-webhook',"opencv-python", 'pyautogui', 'pillow']

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
from discord_webhook import DiscordWebhook, DiscordEmbed
import pyautogui



root = tk.Tk()

# dark mode
root.configure(bg='black')
root.tk_setPalette(background='black', foreground='white')


# variables for the settings
Viplink = tk.StringVar()
LoadingWaitTime = tk.IntVar()
webhooklink = tk.StringVar()
discordid = tk.StringVar()

# function to load settings from the JSON file
def load_settings():
    try:
        with open("settingsnorpc.json", "r") as file:
            settings = json.load(file)
            Viplink.set(settings.get("Viplink", ""))
            LoadingWaitTime.set(settings.get("LoadingWaitTime", 0))
            webhooklink.set(settings.get("webhooklink", ""))
            discordid.set(settings.get("discordid", ""))
    except FileNotFoundError:
        pass


# function to save settings to the JSON file
def submit():
    global Viplink, LoadingWaitTime, webhooklink, client_id, discordid
    Viplink = entry_viplink.get()
    LoadingWaitTime = int(entry_loadingtime.get())
    webhooklink = entry_webhooklink.get()
    discordid = entry_discordid.get()
    
    # save the settings to a JSON file
    settings = {
        "Viplink": Viplink,
        "LoadingWaitTime": LoadingWaitTime,
        "webhooklink": webhooklink,
        "discordid": discordid
    }
    
    with open("settingsnorpc.json", "w") as file:
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


label_webhooklink = tk.Label(root, text="Webhook Link:", bg="black", fg="white")
label_webhooklink.pack()
entry_webhooklink = tk.Entry(root, textvariable=webhooklink, bg="black", fg="white")
entry_webhooklink.pack()


label_discordid = tk.Label(root, text="Discord ID:", bg="black", fg="white")
label_discordid.pack()
entry_discordid = tk.Entry(root, textvariable=discordid, bg="black", fg="white")
entry_discordid.pack()

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


def Webhook(description):
    webhook = DiscordWebhook(url=webhooklink)
    embed = DiscordEmbed(description=description)
    webhook.add_embed(embed)
    webhook.execute()
    
    
def send_disconnected_message(webhooklink, discordid, description=str):
    webhook = DiscordWebhook(url=webhooklink)
    message = f"<@{discordid}>"
    webhook.content = message
    embed = DiscordEmbed(color=0xFF0000)  # Red color
    embed.description = description
    webhook.add_embed(embed)
    webhook.execute()

    
def UpdateTotal():
    global TotalRounds
    TotalRounds += 1

    
def JoinVip():
    Webhook("Hello and thank you for using Ada's Halloween Macro!")
    webbrowser.open(Viplink)
    playbutton = pyautogui.locateOnScreen('Play.png', confidence=0.5)
    while True:
        time.sleep(1)
        Webhook(description="Joining Vip Server")
        time.sleep(LoadingWaitTime)
        if playbutton is not None:
            print("I can see it")
            Webhook(description="Going to Portal")
            autoit.mouse_click("left", x=157, y=482) # Play
            time.sleep(1)
            key.press("a")
            key.press("space")
            time.sleep(10) # can do longer if ur internet slow
            key.release("a")
            key.release("space")
            break
        else: 
            send_disconnected_message(webhooklink=webhooklink, discordid=discordid, description="Yo bro before u go to sleep or outside check ur PC and restart macro, i think roblox failed starting lmao.")
            continue
        

def CheckIfDisconnected():
    disconnectedimg = pyautogui.locateOnScreen('Disconnected.png', confidence=0.6)
    if disconnectedimg is not None:
        send_disconnected_message(webhooklink=webhooklink, discordid=discordid, description="Disconnected in game because of tp fail or internet, restarting.")
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


send_disconnected_message(webhooklink=webhooklink, discordid=discordid, description="Before macro starts you must know something.\nIt's not going to finish Halloween map for you, it only waits for death and restarts.\nYou can increase the amount of candy with Halloween skins or Units.\nThe macro is not going to choose buffs/debuffs(sadly).")


def LobbyMacro():
    JoinVip()
    GameMacro()
    
    
def GameMacro():
    while True:
        Webhook("Discord Rich Presence updated.")
        # autoit.mouse_click("left", x=921, y=174) # Start game (yes button)
        CheckIfJoinedGame()
        Webhook("Image detection(Vote button) pressed yes.")
        CheckIfLost()
        Webhook("Lose Gui Detected")
        UpdateTotal()
        Webhook(f"Total rounds updated: {TotalRounds}") 
        Restart()    
        
        
LobbyMacro()