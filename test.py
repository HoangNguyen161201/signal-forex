import threading
import time

names = []

def check():
    global names
    while True:
        time.sleep(3)
        if(len(names) == 0):
            names.append(len(names) + 1)
            print('right')

def trade():
    global names
    while True:
        for key, info_trade in enumerate(reversed(names)):
            print(info_trade)

thread1 = threading.Thread(target=check)
thread2 = threading.Thread(target=trade)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
    