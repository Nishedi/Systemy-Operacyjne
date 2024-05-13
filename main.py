"""
Main module
"""
import tkinter as tk
from threadsmenager import Threadmenager
from photos import Photos
from player import Player
from map import MapLoader

CANVAS = None  # canvas
ROOT = None  # root of tk
WIDTH = 1880  # base width
HEIGHT = 1160  # base height
START = False  # start of the game, setting true by button
DIFFICULT_MODE = 0  # difficulty mode
CHECK_BOXES = []  # list of difficulty checkboxes


def create_window(window_size, thread_menager_window, map2d):
    """
    Function to create window.
    """
    global CANVAS, ROOT, CHECK_BOXES, WIDTH, HEIGHT
    ROOT = tk.Tk()  # create root
    WIDTH = window_size[1]  # set width
    HEIGHT = window_size[0]  # set height
    ROOT.title("Zombie hunter")  # set title
    ROOT.geometry(f"{568}x{320}")  # set size of welcome page
    start_frame = tk.Frame(ROOT)  # create frame of welcome page
    sub_frame_checkboxes = tk.Frame(start_frame)  # create frame of checkboxes
    # create label with goal
    goal_label = tk.Label(start_frame, text="Your goal is to destroy as many enemies as possible.")
    goal_label.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)  # pack label
    # create label with sterings
    sterings_label = tk.Label(start_frame, text="Use arrows to move and space to shoot.")
    sterings_label.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)  # pack label
    # create label with instruction
    instruction_label = tk.Label(start_frame, text="Press start to begin.")
    instruction_label.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)  # pack label
    # pack frame of checkboxes
    sub_frame_checkboxes.pack(padx=25, pady=5, fill=tk.BOTH, expand=True)
    # create checkbox for easy difficulty
    CHECK_BOXES.append(tk.Checkbutton(sub_frame_checkboxes, text="Easy",
                                      command=lambda: select_difficulty(0)))
    CHECK_BOXES.append(tk.Checkbutton(sub_frame_checkboxes, text="Medium",
                                      command=lambda: select_difficulty(1)))
    CHECK_BOXES.append(tk.Checkbutton(sub_frame_checkboxes, text="Hard",
                                      command=lambda: select_difficulty(2)))
    # create label with select difficulty
    label = tk.Label(sub_frame_checkboxes, text="Select difficulty:")
    label.pack()  # pack label
    CHECK_BOXES[0].select()  # select easy difficulty
    for i in CHECK_BOXES:  # pack all checkboxes
        i.pack()
    button = tk.Button(start_frame, text="Start", width=40, height=2,  # create start button
                       command=lambda: start_game(start_frame, thread_menager_window, map2d))
    button.pack()  # pack start button
    start_frame.place(relx=0.5, rely=0.5, anchor="center")  # place start frame
    CANVAS = tk.Canvas(ROOT, width=WIDTH, height=HEIGHT, bg="white")  # create canvas


def select_difficulty(who_called):
    """
    Function to select difficulty.
    """
    global DIFFICULT_MODE  # global difficulty mode
    if who_called == 0:  # if easy difficulty was selected
        DIFFICULT_MODE = 0  # set difficulty mode to easy
        CHECK_BOXES[1].deselect()  # deselect medium difficulty
        CHECK_BOXES[2].deselect()  # deselect hard difficulty
    if who_called == 1:  # if medium difficulty was selected
        DIFFICULT_MODE = 1  # set difficulty mode to medium
        CHECK_BOXES[0].deselect()  # deselect easy difficulty
        CHECK_BOXES[2].deselect()  # deselect hard difficulty
    if who_called == 2:  # if hard difficulty was selected
        DIFFICULT_MODE = 2  # set difficulty mode to hard
        CHECK_BOXES[0].deselect()  # deselect easy difficulty
        CHECK_BOXES[1].deselect()  # deselect medium difficulty


def key_press(event):
    """
    Function to steer the player.
    """
    player.steer_player(event)


def on_closing(thread_menager_close):
    """
    Function defining what to do when window is closing.
    """
    print("The window is closing...")
    thread_menager_close.close_all()


def start_game(start_frame, thread_menager_starter, map2d):
    """
    Function starting the game invoked by button.
    """
    global START
    thread_menager_starter.set_difficulty(DIFFICULT_MODE)  # set difficulty
    map2d.set_difficult(DIFFICULT_MODE)  # set difficulty
    START = True  # set start to true
    start_frame.destroy()  # destroy start frame
    ROOT.title("Zombie hunter")
    ROOT.geometry(f"{WIDTH}x{HEIGHT}")  # set size of the game depending on map size
    thread_menager_starter.start_threads()  # start all threads
    CANVAS.pack()  # pack canvas


def main_loop(player_object, photos, thread_menager_loop):
    """
    Function that will be called every 100 ms to update visualisation
    """
    if START:  # if game is started
        CANVAS.delete("border")  # delete all borders
        CANVAS.delete('enemy')  # delete all enemies
        CANVAS.delete('ammo')  # delete all ammos
        for i in range(len(mapObject.map2d)):  # draw all borders, enemies and ammos from map
            for j in range(len(mapObject.map2d[i])):
                if mapObject.map2d[i][j] == 'A':
                    CANVAS.create_image(j * 40, i * 40, anchor='nw',
                                        image=photos.return_ammo(), tags='ammo')
                if mapObject.map2d[i][j] == 'X':
                    CANVAS.create_image(j * 40, i * 40, anchor='nw',
                                        image=photos.return_wall(), tags='border')
                if mapObject.map2d[i][j] == 'E':
                    CANVAS.create_image(j * 40, i * 40, anchor='nw',
                                        image=photos.return_enemy(), tags='enemy')
                if mapObject.map2d[i][j] == 'B':
                    CANVAS.create_rectangle(j * 40 + 19, i * 40 + 19, j * 40 + 21, i * 40 + 21,
                                            fill="black", tags="border")

        CANVAS.delete("player")  # delete player
        # draw player
        CANVAS.create_image(player_object.possition[0] * 40, player_object.possition[1] * 40,
                            anchor='nw', image=player_object.player_image, tags="player")
        CANVAS.delete("bar")  # delete bar
        # draw bar
        CANVAS.create_rectangle(WIDTH - 240, 0, WIDTH, 40, fill="ghostwhite", tags="bar")
        # draw text how many bullets left
        CANVAS.create_text(WIDTH - 80, 25, text="bullets: " +
                                                str(player_object.ammo), fill="black",
                           font=('Helvetica', 15),
                           tags="bar")
        CANVAS.create_text(WIDTH - 198, 25, text="score: " + str(player_object.score),
                           fill="black", font=('Helvetica', 15)
                           , tags="bar")  # draw text how many points player has
        CANVAS.create_rectangle(40, 0, 160, 40, fill="black"
                                , tags="bar")  # draw rectangle for visibility of next bullet
        # draw status of next bullet spawn
        CANVAS.create_rectangle(40, 0, 40 + 120 *
                                (thread_menager_loop.bullet_dropper_status
                                 / thread_menager_loop.bullets_dropper_period),
                                40, fill="darkgoldenrod", tags="bar")
        CANVAS.create_text(100, 20, text="Next bullet", fill="white",
                           font=('Helvetica', 15), tags="bar")  # draw text for next bullet spawn
        CANVAS.create_rectangle(200, 0, 320, 40, fill="black",
                                tags="bar")  # draw rectangle for visibility of next enemy
        CANVAS.create_rectangle(200, 0, 200 + 120 *
                                (thread_menager_loop.mob_spawner_status /
                                 thread_menager_loop.mob_spawner_period),
                                40, fill="olivedrab", tags="bar")  # draw status of next enemy spawn
        CANVAS.create_text(260, 20, text="Next enemy", fill="white",
                           font=('Helvetica', 15), tags="bar")  # draw text for next enemy spawn
    # if game is started and is threads are stopped
    if not thread_menager_loop.is_running and START:
        CANVAS.create_rectangle(WIDTH / 2 - 300, HEIGHT / 2 - 200,
                                WIDTH / 2 + 300, HEIGHT / 2 + 200, fill="black")
        CANVAS.create_text(WIDTH / 2, HEIGHT / 2, text="Koniec gry!", fill="maroon",
                           font=('Helvetica', 50))
    ROOT.after(100, lambda: main_loop(player, photos, thread_menager_loop))  # call main loop again


mapObject = MapLoader("Resources/map.txt")  # load map
thread_menager = Threadmenager(mapObject)  # create thread menager
create_window(mapObject.get_size(), thread_menager, mapObject)  # create window
player = Player(thread_menager, mapObject)  # create player
thread_menager.add_thread(player)  # add player to thread menager

ROOT.bind('<Key>', key_press)  # bind keyboard to steer the player
# bind close button to on_closing function
ROOT.protocol("WM_DELETE_WINDOW", lambda: on_closing(thread_menager))
main_loop(player, Photos(), thread_menager)  # start main loop
ROOT.mainloop()
