import threading
import tkinter as tk
from Enemy import Enemy
from Player import Player
from Map import MapLoader
from tkinter import PhotoImage

root = None
width = 1880
height = 1160


def createWindow(windowSize):
    global canvas, root
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
    for i in range(len(map.map)):
        for j in range(len(map.map[i])):
            if map.map[i][j] == 'X':
                canvas.create_rectangle(j * 40, i * 40, j * 40 + 40, i * 40 + 40, fill="grey", tags="border")
            if map.map[i][j] == 'E':
                global photo
                photo = tk.PhotoImage(file="pictures/mob.png")
                canvas.create_image(j * 40, i * 40, anchor='nw', image=photo, tags="border")
            if map.map[i][j] == 'B':
                canvas.create_rectangle(j * 40+19, i * 40+19, j * 40 + 21, i * 40 + 21, fill="black", tags="border")
    canvas.delete("ammo_text")
    canvas.create_text(width - 75, 25, text="bullets: " + str(player.ammo), fill="black",
                            font=('Helvetica', 15), tags="ammo_text")
    canvas.delete("score")
    canvas.delete("player")
    canvas.create_image(player.possition[0] * 40, player.possition[1] * 40, anchor='nw',
                        image=player.player_image, tags="player")

    root.after(100, lambda : mainLoop(player))


map = MapLoader("Resources/map.txt")
createWindow(map.get_size())
objects = []
root.bind('<Key>', key_press)

player = Player(objects, map.findEmptyPlace(), map.map)
objects.append(player)
enemy = Enemy(map.findEmptyPlace(), map.map)
objects.append(enemy)

def on_closing():
    print("Okno zostało zamknięte.")
    player.isRunning = False
    player.thread.join()
    enemy.isRunning = False
    enemy.thread.join()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
mainLoop(player)
root.mainloop()

# if __name__ == '__main__':