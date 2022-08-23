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
number_registered = False


@sio.event
def connect():
    sio.emit('register_number', car_number)

@sio.on('message')
def got_message(message):
    if number_registered:
        q.put(message)

@sio.on('register_number_response')
def register_number_response(resp):
    if(resp == "Success"):
        q.put(f"Connected to race control as car number {car_number}")
    else:   
        q.put(f"Car number {car_number} already registered, shutting down")
        time.sleep(3)
        exit()

car_number = input("Please insert your car number and press enter:\n")
sio.connect("https://rocky-reaches-49584.herokuapp.com")