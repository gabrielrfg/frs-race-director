import socketio
import pyttsx3

sio = socketio.Client()
engine = pyttsx3.init()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('message', "hello")

@sio.on('message')
def got_message(message):
    print(message)
    engine.say("I will speak this text")
    engine.runAndWait()

sio.connect("https://rocky-reaches-49584.herokuapp.com")