from _thread import start_new_thread
import utime

#temp = 0
import globals

def heron(a):
    """Calculates the square root of a"""
    while True:
        globals.temp = globals.temp + 1
        print("heron",globals.temp)
        utime.sleep(1)

    return 10


def turkey():
    while True:
        globals.temp = globals.temp + 1
        print("turkey",globals.temp)
        utime.sleep(1)
    return None

start_new_thread(heron,(99,))
#start_new_thread(heron,(999,))
start_new_thread(turkey,())

c = input("Type something to quit.")