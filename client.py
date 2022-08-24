import queue
import socketio
import pyttsx3
from queue import Queue
from threading import Thread
import time

q = Queue()

def say_loop():
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    engine.setProperty('rate',150)
    while True:
        item = q.get()
        print(item)
        engine.say(item)
        engine.runAndWait()
        q.task_done()

t = Thread(target=say_loop)
t.daemon = True
t.start()

sio = socketio.Client()
car_number = 0

@sio.event
def connect():
    print("connected")

@sio.on('message')
def got_message(message):
    q.put(message)


#car_number = input("Please insert your car number and press enter:\n")
sio.connect("https://dulcet-answer-360423.nw.r.appspot.com")
