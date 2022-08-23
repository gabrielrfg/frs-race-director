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
        enlisted = True
        send_message("Stop and go penalty")
    else:
        exit()


sio.connect("https://rocky-reaches-49584.herokuapp.com")


