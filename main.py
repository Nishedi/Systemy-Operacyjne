import time

from ThreadsMenager import ThreadMenager
import tkinter as tk
from Photos import Photos
from Player import Player
from Map import MapLoader

root = None
width = 1880
height = 1160
start = False
startTime = time.time()
difficultMode = 0
checkBoxes = []


def createWindow(windowSize, threadMenager, map):
    global canvas, root, photo, checkBoxes, width, height
    root = tk.Tk()
    width = windowSize[1]
    height = windowSize[0]
    root.title("Prosta animacja")
    root.geometry(f"{568}x{320}")
    startFrame = tk.Frame(root)
    subFrameCheckboxes = tk.Frame(startFrame)
    goalLabel = tk.Label(startFrame, text="Your goal is to destroy as many enemies as possible.")
    goalLabel.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)
    steringsLabel = tk.Label(startFrame, text="Use arrows to move and space to shoot.")
    steringsLabel.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)

    instructionLabel = tk.Label(startFrame, text="Press start to begin.")
    instructionLabel.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)


    subFrameCheckboxes.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)
    checkBoxes.append(tk.Checkbutton(subFrameCheckboxes, text="Easy", command=lambda: selectDifficulty(0)))
    checkBoxes.append(tk.Checkbutton(subFrameCheckboxes, text="Medium", command=lambda: selectDifficulty(1)))
    checkBoxes.append(tk.Checkbutton(subFrameCheckboxes, text="Hard", command=lambda: selectDifficulty(2)))
    label = tk.Label(subFrameCheckboxes, text="Select difficulty:")
    label.pack()
    checkBoxes[0].select()
    for i in checkBoxes:
        i.pack()
    button = tk.Button(startFrame, text="Start", width=40, height=2, command=lambda: startGame(startFrame, threadMenager, map))
    button.pack()
    startFrame.place(relx=0.5, rely=0.5, anchor="center")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")


def selectDifficulty(whoCalled):
    global difficultMode
    if whoCalled == 0:
        difficultMode = 0
        checkBoxes[1].deselect()
        checkBoxes[2].deselect()
    if whoCalled == 1:
        difficultMode = 1
        checkBoxes[0].deselect()
        checkBoxes[2].deselect()
    if whoCalled == 2:
        difficultMode = 2
        checkBoxes[0].deselect()
        checkBoxes[1].deselect()


def key_press(event):
    player.steerPlayer(event)


def on_closing(threadMenager):
    print("Okno zostało zamknięte.")
    threadMenager.closeAll()



def startGame(startFrame, threadMenager, map):
    global start
    threadMenager.setDifficulty(difficultMode)
    map.setDifficult(difficultMode)
    canvas.delete("startScreen")
    start = True
    startFrame.destroy()
    root.title("Prosta animacja")
    root.geometry(f"{width}x{height}")
    threadMenager.startThreads()
    canvas.pack()

def mainLoop(player, photos, threadMenager):
    global start
    if start:
        canvas.delete("border")
        canvas.delete('enemy')
        canvas.delete('ammo')
        for i in range(len(map.map)):
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

        canvas.delete("player")
        canvas.create_image(player.possition[0] * 40, player.possition[1] * 40, anchor='nw', image=player.player_image, tags="player")
        canvas.delete("bar")
        canvas.create_rectangle(width - 240, 0, width, 40, fill="white", tags="bar")
        canvas.create_text(width - 80, 25, text="bullets: " + str(player.ammo), fill="black", font=('Helvetica', 15), tags="bar")
        canvas.create_text(width - 198, 25, text="score: " + str(player.score), fill="black", font=('Helvetica', 15), tags="bar")
        canvas.create_rectangle(40, 0, 160, 40, fill="white", tags="bar")
        canvas.create_rectangle(40, 0, 40 + 120 * (threadMenager.bulletDropperStatus / threadMenager.bulletsDropperPeriod), 40, fill="green yellow", tags="bar")
        canvas.create_text(100, 20, text="Next bullet", fill="black", font=('Helvetica', 15), tags="bar")
        canvas.create_rectangle(200, 0, 320, 40, fill="white", tags="bar")
        canvas.create_rectangle(200, 0, 200 + 120 * (threadMenager.mobSpawnerStatus / threadMenager.mobSpawnerPeriod), 40, fill="aqua", tags="bar")
        canvas.create_text(260, 20, text="Next enemy", fill="black", font=('Helvetica', 15), tags="bar")
    if not threadMenager.isRunning and start:
        canvas.create_rectangle(width / 2 - 300, height / 2 - 200, width / 2 + 300, height / 2 + 200, fill="magenta")
        canvas.create_text(width / 2, height / 2, text="Koniec gry!", fill="black",
                           font=('Helvetica', 50))
    root.after(100, lambda: mainLoop(player, photos, threadMenager))

map = MapLoader("Resources/map.txt")
threadMenager = ThreadMenager(map)
createWindow(map.get_size(), threadMenager, map)
player = Player(threadMenager, map.findEmptyPlace(), map)
threadMenager.add_thread(player)

root.bind('<Key>', key_press)
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(threadMenager))
mainLoop(player, Photos(), threadMenager)
root.mainloop()
