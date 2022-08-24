import queue
import socketio
import pyttsx3
from queue import Queue
from threading import Thread
import time


sio = socketio.Client()
secret = "secret"
enlisted = False

def send_message(message):
    sio.emit('message_race_control', message)

@sio.event
def connect():
    sio.emit('enlist_race_control', secret)

@sio.on('enlist_race_control_response')
def enlist_race_control_response(message):
    if message == "success":
        print("enlisted")
        enlisted = True
        send_message("Stop and go penalty")
    else:
        print("failed")
        exit()


sio.connect("https://dulcet-answer-360423.nw.r.appspot.com")


