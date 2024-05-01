from ThreadsMenager import ThreadMenager
import tkinter as tk
from Photos import Photos
from Player import Player
from Map import MapLoader
from tkinter import PhotoImage

root = None
width = 1880
height = 1160


def createWindow(windowSize):
    global canvas, root, photo
    root = tk.Tk()
    width = windowSize[1]
    height = windowSize[0]
    root.title("Prosta animacja")
    root.geometry(f"{width}x{height}")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

def key_press(event):
    player.steerPlayer(event)

def on_closing(threadMenager):
    print("Okno zostało zamknięte.")
    threadMenager.closeAll()
    root.destroy()

def mainLoop(player, photos):
    canvas.delete("border")
    canvas.delete('enemy')
    canvas.delete('ammo')
    for i in range(len(map.map)):
        for j in range(len(map.map[i])):
            # print(map.map[i][j], end="")
            if map.map[i][j] == 'A':
                canvas.create_image(j * 40, i * 40, anchor='nw', image=photos.ammo, tags='ammo')
            if map.map[i][j] == 'X':
                canvas.create_image(j * 40, i * 40, anchor='nw', image=photos.wall, tags='border')
            if map.map[i][j] == 'E':
                canvas.create_image(j * 40, i * 40, anchor='nw', image=photos.enemy, tags='enemy')
            if map.map[i][j] == 'B':
                canvas.create_rectangle(j * 40+19, i * 40+19, j * 40 + 21, i * 40 + 21, fill="black", tags="border")
        # print()
    canvas.delete("ammo_text")
    canvas.delete("score")
    canvas.create_text(width - 75, 25, text="bullets: " + str(player.ammo), fill="black",
                            font=('Helvetica', 15), tags="ammo_text")
    canvas.create_text(width - 150, 25, text="score: " + str(player.score), fill="black",
                       font=('Helvetica', 15), tags="score")

    canvas.delete("player")
    canvas.create_image(player.possition[0] * 40, player.possition[1] * 40, anchor='nw',
                        image=player.player_image, tags="player")

    root.after(100, lambda : mainLoop(player, photos))


map = MapLoader("Resources/map.txt")
createWindow(map.get_size())
threadMenager = ThreadMenager(map)
player = Player(threadMenager, map.findEmptyPlace(), map)
threadMenager.add_thread(player)


root.bind('<Key>', key_press)
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(threadMenager))
mainLoop(player, Photos())
root.mainloop()
