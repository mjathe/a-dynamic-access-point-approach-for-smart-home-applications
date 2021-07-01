import threading
import time

class myThread(threading.Thread):
    def __init__(self, id, name):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name

    def run(self):
        print("starte ", self.id)
        time.sleep(self.id*3)
        print("beende ", self.id)

t1 = myThread(1, "t1")
t2 = myThread(2, "t2")

t1.start()
t2.start()

print("beende main")
