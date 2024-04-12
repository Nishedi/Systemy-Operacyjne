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
width = 1280
height = 720



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


def testThread(objects):

    while True:
        for obj in objects:
            if isinstance(obj, Enemy):
                if obj.possitionChanged:
                    obj.possitionChanged = False
                    canvas.delete("enemy")
                    canvas.create_image(obj.possition[0]*40, obj.possition[1]*40, anchor='nw', image= enemy.image, tags="enemy")
            if isinstance(obj, Player):
                if obj.possitionChanged:
                    obj.possitionChanged = False
                    canvas.delete("player")
                    canvas.create_image(obj.possition[0] * 40, obj.possition[1] * 40, anchor='nw',
                                        image=obj.player_image, tags="player")
            if isinstance(obj, Bullet):
                if obj.possitionChanged:
                    if obj.isRunning == False:
                        print("Bullet already  not running")
                        canvas.delete("rect")
                        objects.remove(obj)
                        continue
                    obj.possionChanged = False
                    canvas.delete("rect")
                    canvas.create_rectangle(obj.possition[0]*40, obj.possition[1]*40, obj.possition[0]*40+40, obj.possition[1]*40+40, fill="black", tags="rect")


        time.sleep(0.01)


def mainLoop(player):
    canvas.delete("ammo_text")
    canvas.create_text(width - 75, 25, text="bullets: " + str(player.ammo), fill="black",
                            font=('Helvetica', 15), tags="ammo_text")
    canvas.delete("score")
    root.after(100, lambda : mainLoop(player))


map = MapLoader("Resources/map.txt")
objects = []
createWindow(map.get_size())





root.bind('<Key>', key_press)
player = Player(canvas, width, height, objects, map.findEmptyPlace())
objects.append(player)
for object in map.get_map():
    objects.append(object)
enemy = Enemy(canvas, objects, map.findEmptyPlace())
objects.append(enemy)

threading.Thread(target=testThread, args=(objects,)).start()

for object in map.get_map():
    canvas.create_rectangle(object.possition[0]*40, object.possition[1]*40, object.possition[0]*40+40, object.possition[1]*40+40, fill="white")
mainLoop(player)
root.mainloop()

# if __name__ == '__main__':