import time

from ThreadsMenager import ThreadMenager
import tkinter as tk
from Photos import Photos
from Player import Player
from Map import MapLoader

root = None # root of tk
width = 1880 # base width
height = 1160 # base height
start = False # start of the game, setting true by button
difficultMode = 0 # difficulty mode
checkBoxes = [] # list of difficulty checkboxes

def createWindow(windowSize, threadMenager, map): # create window
    global canvas, root, checkBoxes, width, height
    root = tk.Tk() # create root
    width = windowSize[1] # set width
    height = windowSize[0] # set height
    root.title("Zombie hunter") # set title
    root.geometry(f"{568}x{320}") # set size of welcome page
    startFrame = tk.Frame(root) # create frame of welcome page
    subFrameCheckboxes = tk.Frame(startFrame)  # create frame of checkboxes
    goalLabel = tk.Label(startFrame, text="Your goal is to destroy as many enemies as possible.") # create label with goal
    goalLabel.pack(padx=25, pady=5, fill=tk.BOTH, expand=True) # pack label
    steringsLabel = tk.Label(startFrame, text="Use arrows to move and space to shoot.") # create label with sterings
    steringsLabel.pack(padx=25, pady=5, fill=tk.BOTH, expand=True) # pack label
    instructionLabel = tk.Label(startFrame, text="Press start to begin.") # create label with instruction
    instructionLabel.pack(padx=25, pady=5, fill=tk.BOTH, expand=True) # pack label
    subFrameCheckboxes.pack(padx=25, pady=5, fill=tk.BOTH, expand=True) # pack frame of checkboxes
    checkBoxes.append(tk.Checkbutton(subFrameCheckboxes, text="Easy", command=lambda: selectDifficulty(0))) # create checkbox for easy difficulty
    checkBoxes.append(tk.Checkbutton(subFrameCheckboxes, text="Medium", command=lambda: selectDifficulty(1))) # create checkbox for medium difficulty
    checkBoxes.append(tk.Checkbutton(subFrameCheckboxes, text="Hard", command=lambda: selectDifficulty(2))) # create checkbox for hard difficulty
    label = tk.Label(subFrameCheckboxes, text="Select difficulty:") # create label with select difficulty
    label.pack() # pack label
    checkBoxes[0].select() # select easy difficulty
    for i in checkBoxes: # pack all checkboxes
        i.pack()
    button = tk.Button(startFrame, text="Start", width=40, height=2, command=lambda: startGame(startFrame, threadMenager, map)) # create start button
    button.pack() # pack start button
    startFrame.place(relx=0.5, rely=0.5, anchor="center") # place start frame
    canvas = tk.Canvas(root, width=width, height=height, bg="white") # create canvas


def selectDifficulty(whoCalled): # select difficulty
    global difficultMode # global difficulty mode
    if whoCalled == 0: # if easy difficulty was selected
        difficultMode = 0 # set difficulty mode to easy
        checkBoxes[1].deselect() # deselect medium difficulty
        checkBoxes[2].deselect() # deselect hard difficulty
    if whoCalled == 1:  # if medium difficulty was selected
        difficultMode = 1 # set difficulty mode to medium
        checkBoxes[0].deselect() # deselect easy difficulty
        checkBoxes[2].deselect() # deselect hard difficulty
    if whoCalled == 2: # if hard difficulty was selected
        difficultMode = 2 # set difficulty mode to hard
        checkBoxes[0].deselect() # deselect easy difficulty
        checkBoxes[1].deselect() # deselect medium difficulty

def key_press(event): # bind keyboad to steer the player
    player.steerPlayer(event)

def on_closing(threadMenager): # define actions to do when user click the close button
    print("The window is closing...")
    threadMenager.closeAll()

def startGame(startFrame, threadMenager, map): # start the game
    global start
    threadMenager.setDifficulty(difficultMode) # set difficulty
    map.setDifficult(difficultMode) # set difficulty
    start = True # set start to true
    startFrame.destroy() # destroy start frame
    root.title("Zombie hunter")
    root.geometry(f"{width}x{height}") # set size of the game depending on map size
    threadMenager.startThreads() # start all threads
    canvas.pack() # pack canvas

def mainLoop(player, photos, threadMenager): # main loop of the game visualisation
    global start
    if start: # if game is started
        canvas.delete("border") # delete all borders
        canvas.delete('enemy') # delete all enemies
        canvas.delete('ammo') # delete all ammos
        for i in range(len(map.map)): # draw all borders, enemies and ammos from map
            for j in range(len(map.map[i])):
                if map.map[i][j] == 'A':
                    canvas.create_image(j * 40, i * 40, anchor='nw', image=photos.ammo, tags='ammo')
                if map.map[i][j] == 'X':
                    canvas.create_image(j * 40, i * 40, anchor='nw', image=photos.wall, tags='border')
                if map.map[i][j] == 'E':
                    canvas.create_image(j * 40, i * 40, anchor='nw', image=photos.enemy, tags='enemy')
                if map.map[i][j] == 'B':
                    canvas.create_rectangle(j * 40 + 19, i * 40 + 19, j * 40 + 21, i * 40 + 21, fill="black",
                                            tags="border")

        canvas.delete("player") # delete player
        canvas.create_image(player.possition[0] * 40, player.possition[1] * 40, anchor='nw', image=player.player_image, tags="player") # draw player
        canvas.delete("bar") # delete bar
        canvas.create_rectangle(width - 240, 0, width, 40, fill="ghostwhite", tags="bar") # draw bar
        canvas.create_text(width - 80, 25, text="bullets: " + str(player.ammo), fill="black", font=('Helvetica', 15), tags="bar") # draw text how many bullets left
        canvas.create_text(width - 198, 25, text="score: " + str(player.score), fill="black", font=('Helvetica', 15), tags="bar") # draw text how many points player has
        canvas.create_rectangle(40, 0, 160, 40, fill="black", tags="bar") # draw rectangle for visibility of next bullet
        canvas.create_rectangle(40, 0, 40 + 120 * (threadMenager.bulletDropperStatus / threadMenager.bulletsDropperPeriod), 40, fill="darkgoldenrod", tags="bar") # draw status of next bullet spawn
        canvas.create_text(100, 20, text="Next bullet", fill="white", font=('Helvetica', 15), tags="bar") # draw text for next bullet spawn
        canvas.create_rectangle(200, 0, 320, 40, fill="black", tags="bar") # draw rectangle for visibility of next enemy
        canvas.create_rectangle(200, 0, 200 + 120 * (threadMenager.mobSpawnerStatus / threadMenager.mobSpawnerPeriod), 40, fill="olivedrab", tags="bar") # draw status of next enemy spawn
        canvas.create_text(260, 20, text="Next enemy", fill="white", font=('Helvetica', 15), tags="bar")    # draw text for next enemy spawn
    if not threadMenager.isRunning and start: # if game is started and is threads are stopped
        canvas.create_rectangle(width / 2 - 300, height / 2 - 200, width / 2 + 300, height / 2 + 200, fill="black")
        canvas.create_text(width / 2, height / 2, text="Koniec gry!", fill="maroon",
                           font=('Helvetica', 50))
    root.after(100, lambda: mainLoop(player, photos, threadMenager)) # call main loop again

map = MapLoader("Resources/map.txt") # load map
threadMenager = ThreadMenager(map) # create thread menager
createWindow(map.get_size(), threadMenager, map) # create window
player = Player(threadMenager, map) # create player
threadMenager.add_thread(player) # add player to thread menager

root.bind('<Key>', key_press) # bind keyboard to steer the player
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(threadMenager)) # bind close button to on_closing function
mainLoop(player, Photos(), threadMenager) # start main loop
root.mainloop()
