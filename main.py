import threading
import tkinter as tk
from tkinter import PhotoImage
from Enemy import Enemy
from Player import Player
from Map import MapLoader
from Bullet import Bullet
import time
from tkinter import PhotoImage

# canvas = None
root = None
direction = 1
directionx = 1
directiony = 1
width = 1880
height = 1160



def createWindow(windowSize):
    global canvas, root
    global direction, directionx, directiony
    root = tk.Tk()
    width = windowSize[1]
    height = windowSize[0]
    root.title("Prosta animacja")
    root.geometry(f"{width}x{height}")
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()



def key_press(event):
    player.steerPlayer(event)

def mainLoop(player):
    canvas.delete("border")
    for i in range(len(map.map2)):
        for j in range(len(map.map2[i])):
            if map.map2[i][j] == 'X':
                canvas.create_rectangle(j * 40, i * 40, j * 40 + 40, i * 40 + 40, fill="white", tags="border")
            if map.map2[i][j] == 'P':
                canvas.create_rectangle(j * 40, i * 40, j * 40 + 40, i * 40 + 40, fill="yellow", tags="border")
            if map.map2[i][j] == 'E':
                canvas.create_rectangle(j * 40, i * 40, j * 40 + 40, i * 40 + 40, fill="green", tags="border")
    canvas.delete("ammo_text")
    canvas.create_text(width - 75, 25, text="bullets: " + str(player.ammo), fill="black",
                            font=('Helvetica', 15), tags="ammo_text")
    canvas.delete("score")
    canvas.delete("player")
    canvas.create_image(player.possition[0] * 40, player.possition[1] * 40, anchor='nw',
                        image=player.player_image, tags="player")

    root.after(100, lambda : mainLoop(player))


map = MapLoader("Resources/map.txt")
objects = []
createWindow(map.get_size())





root.bind('<Key>', key_press)
for object in map.get_map():
    objects.append(object)
player = Player(canvas, width, height, objects, map.findEmptyPlace(),map.map2)
objects.append(player)


enemy = Enemy(canvas, objects, map.findEmptyPlace(), map.map2)
objects.append(enemy)

def on_closing():
    print("Okno zostało zamknięte.")
    stop = True

    player.isRunning = False
    player.thread.join()
    root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)

mainLoop(player)
root.mainloop()

# if __name__ == '__main__':