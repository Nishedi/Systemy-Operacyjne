"""
Module containing the Threadmenager class.
"""
import threading
import time
from enemy import Enemy
class Threadmenager:
    """
    Class to manage threads.
    """
    def __init__(self, map2d):
        """
        ThreadMenager initializer
        """
        self.enemy_threads = [] # this is a list of all enemies nothing more
        self.all_threads = [] # this is a list of all threads that are running to control all game
        self.mutex = threading.Lock() # this is a lock used to protect the list of threads
        self.is_running = False # this is a flag used to stop all threads (including this)
        # this is a thread that will drop bullets
        self.bullets_dropper_thread = threading.Thread(target=self.bullets_dropper, args=(map2d,))
        self.bullet_dropper_status = 0 # 0 - not dropping
        self.bullets_dropper_period = 5 # when dropperStatus reach 5, it will drop bullet
        # this is a thread that will spawn enemies
        self.mob_spawner_thread = threading.Thread(target=self.mob_spawner, args=(map2d,))
        self.mob_spawner_period = 10 # same as above
        self.mob_spawner_status = 0
        self.start_time = time.time()

    def set_difficulty(self, difficulty):
        """
        this is a method that will set difficulty of the game
        """
        if difficulty == 0:
            self.bullets_dropper_period = 5
            self.mob_spawner_period = 10
        if difficulty == 1:
            self.bullets_dropper_period = 7
            self.mob_spawner_period = 7
        if difficulty == 2:
            self.bullets_dropper_period = 10
            self.mob_spawner_period = 5

    def start_threads(self):
        """
        this method will start all threads = start the game
        """
        self.is_running = True
        for thread in self.all_threads:
            thread.start_thread()
        self.bullets_dropper_thread.start()
        self.mob_spawner_thread.start()

    def mob_spawner(self, map2d):
        """
        this is a method that will spawn enemies used in mobSpawner thread
        """
        incrementer = 1
        while self.is_running:
            if time.time()-self.start_time>30*incrementer:
                incrementer+=1
                if self.mob_spawner_period>1:
                    self.mob_spawner_period-=1
            self.mob_spawner_status = 0
            while self.mob_spawner_status < self.mob_spawner_period:
                time.sleep(1)
                self.mob_spawner_status += 1
            enemy = Enemy(map2d, self)
            enemy.start_thread()
            if enemy.is_running:
                self.add_thread(enemy)

    def bullets_dropper(self, map2d):
        """
        this is a method that will drop bullets used in bulletsDropper thread
        """
        while self.is_running:
            self.bullet_dropper_status = 0
            while self.bullet_dropper_status < self.bullets_dropper_period:
                time.sleep(1)
                self.bullet_dropper_status += 1
            try:
                map2d.mutex.acquire()
                possition = map2d.find_empty_place()
                if possition:
                    map2d.update_map(possition[1], possition[0], 'A')
            finally:
                map2d.mutex.release()

    def add_thread(self, thread):
        """
        this is a method that will add thread to the list of threads keeping the list safe
        """
        with self.mutex:
            self.enemy_threads.append(thread)
            self.all_threads.append(thread)

    def remove_thread(self, thread):
        """
        this is a method that will remove thread from the list of threads keeping the list safe
        """
        with self.mutex:
            self.enemy_threads.remove(thread)

    def close_all(self):
        """
        this is a method that will stop all threads = end the game
        """
        if self.is_running:
            self.is_running = False
        if self.bullets_dropper_thread.is_alive():
            self.bullets_dropper_thread.join()
        if self.mob_spawner_thread.is_alive():
            self.mob_spawner_thread.join()

        for thread in self.all_threads:
            if thread.thread.is_alive():
                thread.is_running = False
                thread.thread.join()

    def check_hitting(self, possition):
        """
        this is a method that will check if bullet hit an enemy
        """
        with self.mutex:
            for obj in self.enemy_threads:
                if obj.get_possition() == possition:
                    obj.is_running = False
                    self.enemy_threads.remove(obj)
                    return True
            return False
