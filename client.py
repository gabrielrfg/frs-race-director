import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")
    sio.emit('message', "hello")

@sio.on('message')
def got_message(message):
    print(message)

sio.connect("http://localhost:8080")