import threading
import time
import random

class Test:
    def __init__(self):
        self.global_variable1 = 0
        self.global_variable2 = 0
        self.mutex1 = threading.Lock()
        self.mutex2 = threading.Lock()

        self.thread1Counter = 0
        self.thread2Counter = 0
        thread1 = threading.Thread(target=self.target, args=("Thread1",))
        thread2 = threading.Thread(target=self.target2, args=("Thread2",))
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        print(f"Zmienne globalne po zakończeniu wątków: {self.global_variable1}, {self.global_variable2}")
        print("Koniec programu")

    def target(self, who_called=None):
        for i in range(10):
            self.readVariable2(who_called)
            time.sleep(random.randint(0,1)/10)

    def target2(self, who_called=None):
        for i in range(10):
            self.readVariable(who_called)
            time.sleep(random.randint(0,1)/10)

    def checkValue(self):
        print(f"{self.global_variable1})")


    def readVariable(self, who_called=None):
        locked = False
        while not locked:
            locked = self.mutex1.acquire(blocking=False)
            if locked:
                self.global_variable1 -=1
                time.sleep(0.1)
                print(f"{who_called}: Odczyt zasobu: {self.global_variable1}")
                self.mutex1.release()
            else:
                pass
                # print(f"{who_called}: Sekcja krytyczna 2 - Czekam na odblokowanie zasobu...")

    def readVariable2(self, who_called=None):
        locked = False
        while not locked:
            locked = self.mutex1.acquire(blocking=False)
            if locked:
                self.global_variable1 +=1
                time.sleep(0.1)
                print(f"{who_called}: Odczyt zasobu: {self.global_variable1}")
                self.mutex1.release()
            else:
                pass
                # print(f"{who_called}: Sekcja krytyczna 2 - Czekam na odblokowanie zasobu...")

    def modify_shared_variable1(self, who_called=None):
        locked = self.mutex1.acquire(blocking=False)
        try:
            if locked:
                time.sleep(0.1)
                print(f"{who_called}: Odczyt zasobu: {self.global_variable1}")
                self.global_variable1 += 1
            else:
                pass
                # print(f"{who_called}: Sekcja krytyczna 1 - Czekam na odblokowanie zasobu...")

        finally:
            if locked:
                self.mutex1.release()




if __name__ == "__main__":
    Test()


#dodatkowy muteks ktory zablokuje całą metodę, a metoda będzie jeszcze blokowała sobie mapę innym muteksem